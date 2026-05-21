# Event Timing Calculator - Specification Document

## 1. Executive Summary

**Product Name:** Event Timing Calculator  
**Version:** 1.0  
**Status:** Development (Hackathon)

The Event Timing Calculator is a web-based schedule management tool designed for event organizers, competition coordinators, and athletic directors. It enables rapid calculation of cascading event start times based on realistic competitor throughput, eliminating manual scheduling errors and saving hours of planning time.

---

## 2. Product Overview

### 2.1 One-Liner
A schedule calculator that takes a list of competition events and computes realistic updated start times based on competitor count and average time per athlete.

### 2.2 Problem Statement
Event organizers frequently struggle with:
- Manual scheduling calculations prone to human error
- Inability to quickly adjust timelines when event parameters change
- Lack of visibility into cumulative event durations
- Time-consuming export and distribution workflows

### 2.3 Solution
The Event Timing Calculator automates schedule computation with real-time cascading updates, enabling coordinators to visualize the complete event timeline, make adjustments instantly, and export finalized schedules.

---

## 3. Core Features

### 3.1 Event Input Management
- **Add Events:** Users input event details:
  - Event Name (text, required)
  - Scheduled Start Time (time picker, required)
  - Number of Competitors (integer, required, min: 1)
  - Average Time per Athlete (minutes and seconds, required)
  
- **Edit Events:** Click-to-edit interface for any event field
- **Delete Events:** Remove events from the schedule with confirmation
- **Reorder Events:** Drag-and-drop or arrow buttons to reorder

### 3.2 Automatic Cascade Calculation
When any event parameter changes, the system:
1. Calculates event duration: `Duration = Competitor Count × Average Time per Athlete`
2. Updates that event's end time: `End Time = Start Time + Duration`
3. Cascades the next event's start time: `Next Start Time = Current End Time`
4. Propagates changes through all subsequent events
5. **Real-time Update:** All calculations complete instantly (< 100ms)

### 3.3 Schedule Visualization
- **Data Table Display:**
  - Event Name
  - Scheduled Start Time
  - Competitor Count
  - Average Time per Athlete
  - Calculated Duration
  - Calculated End Time
  - Status indicator (on-time, delayed, etc.)
  
- **Summary Metrics:**
  - Total Event Count
  - Overall Schedule Duration
  - Latest End Time
  - Schedule Start to Finish Duration

### 3.4 Schedule Persistence
- **Save Schedule:** Button to persist current schedule to backend
- **Load Schedule:** Auto-load most recent saved schedule on app startup
- **Database:** Local JSON file (`database.json`) for simplicity

### 3.5 Export Capability
- **CSV Export:** Download schedule as CSV file with all event details
- **Filename:** `schedule_[TIMESTAMP].csv`
- **Format:** Human-readable, one event per row

---

## 4. Technical Architecture

### 4.1 Technology Stack
- **Backend:** Python 3.8+ with FastAPI
- **Frontend:** HTML5, Vanilla JavaScript (ES6+), Tailwind CSS
- **Database:** Local JSON file (database.json)
- **Styling:** Tailwind CSS v3 (via public CDN)
- **Deployment:** Single-machine development environment

### 4.2 Directory Structure
```
project-root/
├── main.py                 # FastAPI application
├── database.json           # Local JSON storage
├── templates/
│   └── index.html         # Frontend interface
└── SPECIFICATION.md       # This file
```

### 4.3 Data Flow
```
User Input (HTML Form)
    ↓
Vanilla JS Event Handler
    ↓
Cascade Calculation Engine (JS)
    ↓
DOM Update (Table Refresh)
    ↓
[User clicks "Save"]
    ↓
POST /api/schedule (JSON)
    ↓
FastAPI Endpoint
    ↓
Write to database.json
    ↓
JSON Response
    ↓
[User clicks "Export"]
    ↓
CSV Generation (JS)
    ↓
Download File
```

---

## 5. Data Model

### 5.1 Event Object
```json
{
  "id": "uuid-or-timestamp",
  "name": "100m Sprint",
  "startTime": "09:00",
  "competitorCount": 24,
  "avgTimeMinutes": 0,
  "avgTimeSeconds": 45,
  "duration": "18:00",
  "endTime": "09:18",
  "durationInSeconds": 1080
}
```

### 5.2 Schedule Object (database.json)
```json
{
  "schedules": [
    {
      "id": "schedule-001",
      "name": "State Track Championship 2026",
      "createdAt": "2026-05-21T14:30:00Z",
      "updatedAt": "2026-05-21T14:35:00Z",
      "events": [
        { "id": "evt-001", "name": "100m Sprint", ... },
        { "id": "evt-002", "name": "200m Sprint", ... }
      ]
    }
  ],
  "currentScheduleId": "schedule-001"
}
```

---

## 6. User Workflows

### 6.1 Create New Schedule
1. User opens application
2. Views empty schedule interface
3. Clicks "Add Event" button
4. Fills in event details (name, start time, competitor count, avg time)
5. Confirms entry
6. Event appears in table with calculated cascade times
7. Repeats for all events

### 6.2 Modify Schedule
1. User clicks on an event field in the table
2. Field becomes editable (inline edit or modal)
3. User changes value and presses Enter/confirms
4. All downstream times auto-calculate
5. Table updates instantly
6. User reviews updated schedule

### 6.3 Save Schedule
1. User finalizes schedule
2. Clicks "Save Schedule" button
3. Backend receives POST request
4. Schedule written to database.json
5. User receives confirmation message
6. Schedule persists across sessions

### 6.4 Export Schedule
1. User clicks "Export to CSV" button
2. JavaScript generates CSV from current table data
3. Browser triggers automatic download
4. File saved as `schedule_[timestamp].csv`
5. User can open in Excel, Sheets, or any CSV viewer

### 6.5 Load Previous Schedule
1. User opens application
2. Most recent saved schedule auto-loads from backend
3. All events and times displayed
4. User can modify or create new schedule

---

## 7. API Specification

### 7.1 GET /api/schedule
**Purpose:** Retrieve the most recent saved schedule

**Request:**
```http
GET /api/schedule HTTP/1.1
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "schedule-001",
    "name": "State Track Championship 2026",
    "createdAt": "2026-05-21T14:30:00Z",
    "updatedAt": "2026-05-21T14:35:00Z",
    "events": [
      {
        "id": "evt-001",
        "name": "100m Sprint",
        "startTime": "09:00",
        "competitorCount": 24,
        "avgTimeMinutes": 0,
        "avgTimeSeconds": 45,
        "durationInSeconds": 1080,
        "endTime": "09:18"
      }
    ]
  }
}
```

**Response (204 No Content):** If no schedule exists (first load)

---

### 7.2 POST /api/schedule
**Purpose:** Save or update the current schedule

**Request:**
```http
POST /api/schedule HTTP/1.1
Content-Type: application/json

{
  "name": "State Track Championship 2026",
  "events": [
    {
      "id": "evt-001",
      "name": "100m Sprint",
      "startTime": "09:00",
      "competitorCount": 24,
      "avgTimeMinutes": 0,
      "avgTimeSeconds": 45,
      "durationInSeconds": 1080,
      "endTime": "09:18"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Schedule saved successfully",
  "data": {
    "id": "schedule-001",
    "savedAt": "2026-05-21T14:35:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid schedule data"
}
```

---

## 8. UI/UX Specifications

### 8.1 Visual Design
- **Theme:** Dark mode (charcoal gray background, white text)
- **Color Palette:**
  - Primary: #3B82F6 (Blue)
  - Success: #10B981 (Green)
  - Warning: #F59E0B (Orange)
  - Danger: #EF4444 (Red)
  - Background: #1F2937 (Dark Gray)
  - Text: #F3F4F6 (Light Gray)

### 8.2 Layout
- **Header:** App title, schedule name (editable), last saved timestamp
- **Left Sidebar (40%):** Event input form
  - Event Name input
  - Start Time time-picker
  - Competitor Count spinner
  - Average Time input (minutes/seconds)
  - Add Event button
  - Save Schedule button
  - Export to CSV button

- **Right Panel (60%):** Schedule table
  - Responsive data table with horizontal scroll on mobile
  - Column headers: Event, Start Time, Duration, End Time, Competitors, Avg Time, Actions
  - Edit/Delete buttons per row
  - Summary metrics footer

### 8.3 Interactions
- **Real-time Validation:** Input fields validate on blur
- **Hover Effects:** Rows highlight on hover; buttons show cursor pointer
- **Loading State:** Buttons show spinner during API calls
- **Toast Notifications:** Brief success/error messages (auto-dismiss after 3 seconds)
- **Keyboard Support:** Tab navigation, Enter to confirm, Esc to cancel

---

## 9. Cascade Calculation Algorithm

### 9.1 Calculation Logic
```
For each event in sequence:
  1. Parse startTime to minutes (e.g., "09:00" → 540)
  2. Calculate duration = competitorCount × (avgTimeMinutes × 60 + avgTimeSeconds)
  3. Calculate endTime = startTime + duration (in seconds)
  4. Set next event's startTime = current event's endTime
  5. Format times back to HH:MM format
  6. Update DOM
```

### 9.2 Time Format Handling
- **Input Format:** HH:MM (24-hour)
- **Storage Format:** Total seconds from midnight
- **Display Format:** HH:MM (24-hour)
- **Cross-Day Handling:** If end time exceeds 23:59, display as next day with indicator

---

## 10. Error Handling

### 10.1 Input Validation
- Event name: Required, non-empty string
- Start time: Valid time format (HH:MM)
- Competitor count: Integer ≥ 1
- Average time: Non-negative (minutes ≥ 0, seconds 0-59)

### 10.2 API Error Handling
- **Network Errors:** Display "Connection failed" message; retry available
- **Invalid Data:** Display specific error message to user
- **Server Errors:** Display generic "Something went wrong" + contact admin message

### 10.3 Edge Cases
- **Cross-midnight Schedules:** Display "next day" indicator for events after 00:00
- **Very Long Events:** Support events > 1 hour without issue
- **Empty Schedule:** Allow save; auto-load on next session
- **Duplicate Event Names:** Allowed (use UUID for tracking)

---

## 11. Performance & Scalability

### 11.1 Performance Targets
- Cascade recalculation: < 100ms for 50+ events
- Page load: < 2 seconds
- API response time: < 500ms
- CSV generation: < 1 second

### 11.2 Scalability Considerations
- **Current Scope:** Single user, local JSON storage
- **Future:** Multi-user support via database (PostgreSQL)
- **Future:** WebSocket for real-time collaboration
- **Limitations:** JSON storage adequate for < 1000 events per schedule

---

## 12. Testing Requirements

### 12.1 Functional Tests
- [ ] Add event with all fields
- [ ] Cascade updates when competitor count changes
- [ ] Cascade updates when average time changes
- [ ] Cascade updates when start time changes
- [ ] Delete event and verify cascade resets
- [ ] Save schedule persists data
- [ ] Load schedule retrieves saved data
- [ ] Export generates valid CSV

### 12.2 Edge Case Tests
- [ ] Cross-midnight event sequences
- [ ] Single event schedule
- [ ] Very large competitor counts (1000+)
- [ ] Very short average times (< 1 second)
- [ ] Simultaneous event modifications
- [ ] Long event names (100+ characters)

---

## 13. Future Enhancements

- Multi-schedule management (save and switch between schedules)
- Team/multi-user collaboration with real-time sync
- Event categories or heat divisions
- Athlete registration integration
- Email schedule distribution
- Mobile app version
- Print-friendly schedule view
- Schedule templating for recurring events
- Analytics dashboard (event duration trends, etc.)

---

## 14. Definitions & Glossary

- **Cascade Calculation:** Automatic propagation of time updates through dependent events
- **Competitor Count:** Number of athletes participating in an event
- **Average Time per Athlete:** Expected duration for one competitor to complete an event
- **Event Duration:** Total time for all competitors: `Count × Avg Time`
- **End Time:** Calculated finish time for an event: `Start Time + Duration`
- **Schedule Persistence:** Saving schedule to local storage (JSON file)

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-21  
**Author:** Development Team
