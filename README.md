# ⏱️ Event Timing Calculator

A simple web app that helps you create and manage competition schedules by automatically calculating how long each event will take and when the next one should start.

## What Does This App Do?

Imagine you're running a track meet or sports competition with multiple events. Each event has:
- A name (e.g., "100m Sprint")
- A start time (e.g., 9:00 AM)
- A number of competitors (e.g., 24 athletes)
- How long each athlete takes (e.g., 45 seconds)

The **Event Timing Calculator** instantly tells you:
- How long the entire event will take (competitors × time per athlete)
- When that event will end
- When the next event should start
- Your complete schedule from start to finish

**Best part:** Change any number and the entire schedule updates automatically. No manual math needed.

## Key Features

✅ **Instant Schedule Calculation** – Add events and see times automatically cascade  
✅ **Real-Time Updates** – Change a competitor count or time and watch the schedule adjust  
✅ **Save Your Schedule** – Stores schedules locally so you don't lose your work  
✅ **Export to CSV** – Download your schedule as a spreadsheet (Excel, Google Sheets, etc.)  
✅ **Dark Mode UI** – Modern, easy-to-read interface  
✅ **No Database Setup** – Everything runs locally on your machine  

## How to Run It

### Prerequisites
- Python 3.8 or higher ([download here](https://www.python.org/downloads/))
- A web browser

### Step 1: Install Dependencies
Open a terminal/command prompt and run:
```bash
pip install fastapi uvicorn
```

### Step 2: Start the Server
In the project folder, run:
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Open in Browser
Go to: **http://localhost:8000**

That's it! The app is ready to use.

## How to Use

### Adding Events
1. **Enter Event Name** – Type a name like "100m Sprint"
2. **Set Start Time** – Pick the time the event should start (e.g., 9:00 AM)
3. **Enter Competitor Count** – How many athletes are running this event
4. **Set Average Time** – How long (in seconds) each athlete takes
5. **Click "Add Event"** – The event appears in the table on the right

### Cascade Effect
Once you add an event, the app automatically:
- Calculates how long that event takes
- Shows when it ends
- Updates the next event's start time

If you change any number, the entire schedule recalculates instantly.

### Saving Your Schedule
- Click **"Save Schedule"** to store your work
- The schedule saves to a local file (`database.json`)
- When you reload the page, your schedule loads automatically

### Exporting Your Schedule
- Click **"Export to CSV"** to download your schedule
- Opens in Excel, Google Sheets, or any spreadsheet app
- Perfect for sharing with other organizers

### Editing Events
- Click any time, competitor count, or average time to change it
- The schedule updates instantly
- Delete an event with the **Delete** button

## Example Workflow

**You're running a school track meet with 3 events:**

1. Add "100m Sprint" at 9:00 AM, 24 competitors, 45 seconds each
   - Duration: 18 minutes (24 × 45 sec)
   - Ends: 9:18 AM

2. Add "200m Sprint" at 9:18 AM (auto-cascaded!), 24 competitors, 90 seconds each
   - Duration: 36 minutes
   - Ends: 9:54 AM

3. Add "400m Sprint" at 9:54 AM, 20 competitors, 120 seconds each
   - Duration: 40 minutes
   - Ends: 10:34 AM

**Your complete schedule is ready in seconds.** Change the competitor count for any event and all downstream times update automatically.

## Technical Details

- **Backend:** Python with FastAPI
- **Frontend:** HTML, CSS (Tailwind), and JavaScript
- **Storage:** Local JSON file (no database needed)
- **No Sign-Up:** Runs entirely on your machine

## Files

- `main.py` – The backend server
- `templates/index.html` – The web interface
- `database.json` – Your saved schedules (auto-created)
- `SPECIFICATION.md` – Complete technical documentation

## Need Help?

- **App won't start?** Make sure Python is installed and you ran `pip install fastapi uvicorn`
- **Page won't load?** Check that http://localhost:8000 is the correct URL and the server is running
- **Lost your schedule?** It's saved in `database.json` — don't delete that file
- **Want to clear everything?** Delete `database.json` and restart the server

## Future Ideas

- Multi-user collaboration
- Email schedule notifications
- Mobile app version
- Team management
- Integration with registration systems

---

**Created for Hackathon** | Built with ❤️ using Python and FastAPI