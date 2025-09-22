# Design

## UI/UX

- **Theme:** Modern, clean, and motivational.
- **Colors:** Use a vibrant and inspiring color palette.
- **Layout:**
  - Main window with a navigation bar on the left.
  - Content area on the right to display the selected view (dashboard, projects, or tasks).
- **Typography:** Use clear and readable fonts.
- **Icons:** Use icons to enhance usability and visual appeal.

## Data Structure

- `projects.json`:
  ```json
  [
    {
      "id": 1,
      "name": "Project 1",
      "description": "This is the first project."
    }
  ]
  ```
- `tasks.json`:
  ```json
  [
    {
      "id": 1,
      "project_id": 1,
      "name": "Task 1",
      "due_date": "2025-10-01",
      "completed": false
    }
  ]
  ```