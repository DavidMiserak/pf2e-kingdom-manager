# Kingdoms App Refactoring Plan

## Context

The PF2E Kingdom Manager has completed Phase 1-2 implementation with 129 tests at 97% coverage. The kingdoms app has grown to a substantial size with some code duplication and optimization opportunities across models, views, forms, and templates.

This refactoring focuses on **high-impact, low-risk improvements** that reduce duplication, improve performance, and maintain code quality without introducing breaking changes. More invasive changes (like ruin/commodity normalization via JSONField) are intentionally deferred until Phase 3 (territory management) is complete.

---

## Refactoring Goals

1. **Performance**: Add database indexes to optimize critical queries
2. **Code Quality**: Eliminate duplicate patterns across views, forms, and templates
3. **Maintainability**: Extract reusable components and utilities
4. **Safety**: Maintain 97% test coverage and avoid breaking changes

---

## Phase 1: High Impact, Low Risk

### 1.1 Add Database Indexes

**Problem**: Every kingdom view executes `KingdomMembership.objects.get(user=request.user, kingdom=self.kingdom)` (line 18-20 in mixins.py) without an index. Turn and activity queries also lack indexes on frequently-used columns.

**Solution**: Add compound indexes to optimize membership lookups, turn queries, and activity queries.

**Files to Modify**:

- `kingdoms/models.py` (add Meta.indexes)
- New migration file

**Changes**:

```python
# KingdomMembership - add to Meta class
indexes = [
    models.Index(fields=["kingdom", "user"]),  # Mixin lookup pattern
]

# KingdomTurn - add to Meta class
indexes = [
    models.Index(fields=["kingdom", "-turn_number"]),  # Turn list queries
    models.Index(fields=["kingdom", "completed_at"]),  # Current turn lookup
]

# ActivityLog - add to Meta class
indexes = [
    models.Index(fields=["turn", "-created_at"]),  # Activity ordering
]
```

**Impact**: Optimizes ALL kingdom views (every request uses membership lookup), speeds up turn/activity queries.

**Testing**: Run full test suite after migration; verify no regressions.

---

### 1.2 Cache Size Calculation

**Problem**: `_size_info()` method (line 432) is called 3x per kingdom display via `size_category`, `commodity_storage_limit`, and `resource_die_type` properties, but recalculates each time.

**Solution**: Use `@cached_property` from `functools` to cache the result.

**Files to Modify**:

- `kingdoms/models.py` (Kingdom model)

**Changes**:

```python
from functools import cached_property

@cached_property
def _size_info(self):
    count = self.hex_count
    for max_hexes, label, storage, die in SIZE_CATEGORIES:
        if max_hexes is None or count <= max_hexes:
            return label, storage, die
    return SIZE_CATEGORIES[-1][1:]
```

**Impact**: Reduces 3 function calls to 1 per request; no external API change.

**Testing**: Existing property tests verify output unchanged.

---

### 1.3 Extract Template Includes

**Problem**: Form templates repeat the same breadcrumb + card wrapper pattern (~46 lines each) across `turn_form.html`, `activity_form.html`, and `turn_confirm_delete.html`. Page headers with back buttons are duplicated across `leadership_form.html`, `skills_form.html`, and `member_list.html`.

**Solution**: Create reusable template includes for common patterns.

**Files to Create**:

- `templates/kingdoms/_includes/form_card_wrapper.html`
- `templates/kingdoms/_includes/page_header_back_button.html`

**Files to Modify**:

- `templates/kingdoms/turn_form.html`
- `templates/kingdoms/activity_form.html`
- `templates/kingdoms/turn_confirm_delete.html`
- `templates/kingdoms/leadership_form.html`
- `templates/kingdoms/skills_form.html`
- `templates/kingdoms/member_list.html`

**Pattern Example** (form_card_wrapper.html):

```django
{# Reusable card wrapper with breadcrumb navigation #}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        {% if breadcrumb_items %}
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                {% for item in breadcrumb_items %}
                <li class="breadcrumb-item{% if item.active %} active{% endif %}">
                    {% if item.url %}<a href="{{ item.url }}">{{ item.label }}</a>
                    {% else %}{{ item.label }}{% endif %}
                </li>
                {% endfor %}
            </ol>
        </nav>
        {% endif %}
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-transparent border-bottom-0 pt-4">
                <h4><i class="fa-solid fa-{{ icon }} me-2"></i>{{ title }}</h4>
            </div>
            <div class="card-body">
                {{ content }}
            </div>
        </div>
    </div>
</div>
```

**Impact**: ~100-150 lines eliminated across templates; consistent styling; easier future UI changes.

**Testing**: Visual regression testing; verify all forms render correctly.

---

## Phase 2: Code Quality Improvements

### 2.1 Extract URL Generation Helper

**Problem**: 16+ instances of duplicate `reverse()` calls like:

```python
reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
reverse("kingdoms:turn_detail", kwargs={"pk": self.kingdom.pk, "turn_pk": turn.pk})
```

**Solution**: Create utility module with helper functions.

**Files to Create**:

- `kingdoms/url_helpers.py`

**Files to Modify**:

- `kingdoms/views.py` (all views with reverse() calls)

**Changes**:

```python
# url_helpers.py
from django.urls import reverse

def kingdom_url(name, kingdom_pk, **kwargs):
    """Generate kingdoms: namespace URL with kingdom pk."""
    return reverse(f"kingdoms:{name}", kwargs={"pk": kingdom_pk, **kwargs})

def turn_url(name, kingdom_pk, turn_pk, **kwargs):
    """Generate turn-specific URL."""
    return reverse(f"kingdoms:{name}",
                   kwargs={"pk": kingdom_pk, "turn_pk": turn_pk, **kwargs})

# Usage in views
# Before: reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
# After: kingdom_url("kingdom_detail", self.kingdom.pk)
```

**Impact**: ~16 call sites simplified; centralized URL pattern logic.

**Testing**: Existing view tests verify URLs unchanged.

---

### 2.2 Consolidate Choice Generator Functions

**Problem**: Three functions (`_charter_choices`, `_heartland_choices`, `_government_choices` in forms.py lines 25-58) follow identical patterns with different data sources.

**Solution**: Create generic helper that accepts formatter function.

**Files to Modify**:

- `kingdoms/forms.py`

**Changes**:

```python
def _build_enum_choices_with_effects(enum_class, formatter, *, include_blank=True):
    """Generic choice builder for enums with effect annotations.

    Args:
        enum_class: The enum to build choices from
        formatter: Function that takes enum value and returns effect string
        include_blank: Whether to include blank option
    """
    choices = [("", "None" if not include_blank else "---------")]
    for item in enum_class:
        effect_str = formatter(item)
        choices.append((item.value, f"{item.label}{effect_str}"))
    return choices

def _format_charter_effects(charter):
    effects = CHARTER_EFFECTS[charter]
    parts = []
    if effects["boost"]:
        parts.append(f"+{effects['boost'].label}")
    if effects["flaw"]:
        parts.append(f"−{effects['flaw'].label}")
    return f" ({', '.join(parts)})" if parts else ""

def _charter_choices(*, include_blank=True):
    return _build_enum_choices_with_effects(
        Charter, _format_charter_effects, include_blank=include_blank
    )

# Similar for _heartland_choices and _government_choices
```

**Impact**: ~40 lines reduced; pattern reusable for future enums.

**Testing**: Form tests verify choices unchanged; check rendering in create/update forms.

---

### 2.3 Extract Formset Handling Mixin

**Problem**: `LeadershipUpdateView` (lines 123-149) and `SkillsUpdateView` (lines 152-180) duplicate ~30 lines of formset GET/POST logic.

**Solution**: Create generic formset mixin.

**Files to Modify**:

- `kingdoms/mixins.py` (add new mixin)
- `kingdoms/views.py` (simplify LeadershipUpdateView and SkillsUpdateView)

**Changes**:

```python
# mixins.py - add new mixin
class FormsetViewMixin:
    """Generic mixin for modelformset_factory-based views."""
    formset_class = None
    success_message = "Updated successfully."

    def get_formset_queryset(self):
        """Override to provide queryset for formset."""
        raise NotImplementedError

    def get_formset_kwargs(self):
        return {"queryset": self.get_formset_queryset()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = self.formset_class(**self.get_formset_kwargs())
        return context

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, **self.get_formset_kwargs())
        if formset.is_valid():
            formset.save()
            messages.success(request, self.success_message)
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(formset=formset))

# views.py - simplified LeadershipUpdateView
class LeadershipUpdateView(FormsetViewMixin, GMRequiredMixin, TemplateView):
    template_name = "kingdoms/leadership_form.html"
    formset_class = LeadershipFormSet
    success_message = "Leadership assignments updated."

    def get_formset_queryset(self):
        return self.kingdom.leadership_assignments.all()

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["form_kwargs"] = {"kingdom": self.kingdom}
        return kwargs

    def get_success_url(self):
        return kingdom_url("kingdom_detail", self.kingdom.pk)
```

**Impact**: ~30 lines eliminated per view (2 views = 60 lines saved); consistent formset handling.

**Testing**: Existing view tests verify behavior unchanged; POST validation and error handling preserved.

---

## Deferred Items

The following opportunities were identified but are intentionally deferred:

### Ruin/Commodity JSONField Normalization

**Why Defer**: Requires data migration; current structure works fine; Phase 3 may introduce new patterns that inform the design.

### CreatorOrGMRequiredMixin

**Why Defer**: Only 2 use cases; explicit permission checks are clearer for security-critical code; pattern may evolve in Phase 3.

### Custom Model Managers

**Why Defer**: Current inline queries are clear; no compelling use case for abstraction yet.

### Complex View Logic Extraction

**Why Defer**: `KingdomDetailView.get_context_data()` works fine; no urgent need to extract to model methods.

---

## Implementation Order

1. **Add database indexes** (1.1) - CRITICAL performance optimization
2. **Cache size calculation** (1.2) - Quick win, 5 minutes
3. **Extract template includes** (1.3) - UI consistency
4. **URL helper utility** (2.1) - Foundation for other changes
5. **Choice generator consolidation** (2.2) - Forms cleanup
6. **Formset mixin** (2.3) - View simplification

---

## Testing Strategy

For each change:

1. Run `make test` BEFORE changes (establish baseline)
2. Make changes incrementally
3. Run `make test` after each logical unit
4. Verify coverage remains at 97%
5. Visual testing for template changes

For database indexes (1.1):

```bash
make migrate  # Apply forward migration
make test     # Verify all tests pass
# Manually test rollback:
podman compose exec web python manage.py migrate kingdoms <previous_migration>
make test     # Verify rollback works
make migrate  # Re-apply forward
```

---

## Critical Files

- `/home/david/projects/pf2e-kingdom-manager/kingdoms/models.py` - Indexes, cached property
- `/home/david/projects/pf2e-kingdom-manager/kingdoms/mixins.py` - Formset mixin
- `/home/david/projects/pf2e-kingdom-manager/kingdoms/forms.py` - Choice consolidation
- `/home/david/projects/pf2e-kingdom-manager/kingdoms/views.py` - URL helpers, formset usage
- `/home/david/projects/pf2e-kingdom-manager/templates/kingdoms/turn_form.html` - Template include reference
- `/home/david/projects/pf2e-kingdom-manager/templates/kingdoms/leadership_form.html` - Formset pattern reference

---

## Expected Outcomes

- **Performance**: Database queries optimized with indexes on hot paths
- **Code reduction**: ~200+ lines eliminated across views, forms, templates
- **Maintainability**: Reusable components for forms, URLs, templates
- **Test coverage**: Maintained at 97%
- **Zero breaking changes**: All existing functionality preserved
