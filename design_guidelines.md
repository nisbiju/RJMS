# Educational Q&A App - Design Guidelines

## Design Approach

**Selected System:** Material Design with Notion/Linear productivity influences for the editing experience. This combination provides clear visual hierarchy for content-dense educational material while delivering intuitive editing capabilities that feel modern and efficient.

**Core Principles:**
- Clarity and readability for educational content
- Efficient content management workflows
- Clear visual feedback for all interactions
- Scannable question/answer hierarchies

## Typography System

**Font Families:**
- Primary: Inter (via Google Fonts) - UI elements, navigation, labels
- Content: Source Serif Pro (via Google Fonts) - Questions and answers for enhanced readability

**Hierarchy:**
- Page Titles: 2.5rem (40px), semibold, tight letter-spacing
- Section Headers: 1.5rem (24px), medium weight
- Question Text: 1.125rem (18px), regular weight, Source Serif Pro
- Answer Options: 1rem (16px), regular weight
- Labels/Meta: 0.875rem (14px), medium weight
- Buttons/Actions: 0.9375rem (15px), medium weight

## Layout System

**Spacing Primitives:** Tailwind units of 2, 4, 6, and 8 for consistent rhythm
- Component padding: p-6
- Section spacing: gap-8 or space-y-8
- Card spacing: p-8
- Tight spacing: gap-4
- Form elements: space-y-6

**Grid Structure:**
- Main container: max-w-6xl mx-auto px-6
- Two-column layout for desktop (question list + detail view)
- Sidebar: w-80 (320px) for filters/navigation
- Content area: flex-1 for primary content

## Component Library

### Navigation & Header
- Fixed top navigation bar with app branding (left), search bar (center), and create button (right)
- Height: h-16
- Search bar: Prominent, expands to w-96 on focus
- Primary CTA: "Create Question" button with icon

### Question List View
- Card-based layout with elevated appearance
- Each card displays:
  - Question text (truncated to 2 lines)
  - Number of answers
  - Correct answer indicator (checkmark badge)
  - Last edited timestamp
  - Quick action icons (edit, delete) on hover
- Card spacing: gap-4 in vertical list
- Pagination or infinite scroll for large lists

### Question Detail/Edit Interface
- Split-pane design:
  - Left: Question editor with rich text capabilities
  - Right: Answer options list with drag-to-reorder
- Question editor: Large text area with min-h-32
- Answer input: List of answer cards with:
  - Text input field
  - Radio button to mark as correct
  - Delete icon
  - Drag handle for reordering
- "Add Answer" button at bottom of answer list

### Search & Filter Panel
- Sticky sidebar with:
  - Search input at top
  - Filter chips for question status (all, answered, unanswered)
  - Sort dropdown (newest, oldest, most answers)
  - Category tags if applicable

### Forms & Inputs
- Floating label style for text inputs
- Input fields: h-12 with rounded-lg borders
- Textarea: min-h-24 for question input
- Radio buttons: Larger touch targets (w-5 h-5)
- Checkboxes: Custom styled with checkmark icon

### Action Buttons
- Primary: Filled style with subtle shadow
- Secondary: Outlined style
- Danger: Outlined with warning indication
- Icon buttons: w-10 h-10 circular with centered icons
- Button groups: gap-3 for spacing

### Cards & Containers
- Standard card: rounded-xl with subtle elevation
- Hover state: Slight elevation increase
- Active/selected: Highlighted border treatment
- Padding: p-6 for standard cards, p-8 for detail views

### Modals & Overlays
- Delete confirmation: Centered modal with max-w-md
- Success notifications: Top-right toast notifications
- Modal backdrop: Semi-transparent overlay
- Modal content: rounded-2xl with generous padding (p-8)

### Status Indicators
- Correct answer badge: Small pill with checkmark icon
- Answer count: Circular badge showing number
- Timestamps: Subtle text with clock icon
- Empty states: Centered illustration with helpful text

### Icons
**Library:** Heroicons (via CDN)
- Navigation: outline style, 24px
- Actions: outline style, 20px
- Status indicators: solid style, 16px
- Consistent icon usage: edit (pencil), delete (trash), add (plus), search (magnifying glass), correct (check-circle)

## Responsive Behavior

**Desktop (lg and above):**
- Two-column layout: sidebar + main content
- Question detail opens in right pane
- Persistent filters and search

**Tablet (md):**
- Single column with collapsible sidebar
- Question detail replaces list view
- Back button to return to list

**Mobile:**
- Stacked single-column layout
- Bottom navigation for key actions
- Simplified filters in dropdown
- Full-screen question editor

## Interaction Patterns

**Question Management:**
- Click question card to open detail view
- Inline editing with "Edit" button toggle
- Auto-save indicator during editing
- Clear save/cancel actions

**Answer Management:**
- Add answers with visible "+ Add Answer" button
- Drag handles for reordering (desktop only)
- Single radio selection for correct answer
- Immediate visual feedback on selection

**Deletion:**
- Two-step confirmation for question deletion
- Single-click deletion for answers (with undo option)
- Clear destructive action styling

## Images

**Hero Section:** No large hero image - this is a productivity tool focused on immediate functionality

**Empty States:**
- Illustration for "No questions yet" state
- Simple, friendly educational-themed graphics
- Placed in center of empty question list area
- Dimensions: approximately 200x200px, centered with message below

**Icons Only:** All other visuals use icon library - no decorative images needed for this utility-focused application