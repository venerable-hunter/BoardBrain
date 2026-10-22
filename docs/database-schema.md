# Database Schema

## Database Choice: SQLite

### Why SQLite?
- **Zero configuration** - No separate database server needed
- **Single file** - Database is stored as a single file on disk
- **Perfect for MVP** - Easy to set up, no infrastructure overhead
- **Sufficient for our needs** - Handles multiple users and boards easily
- **Portable** - Easy to backup and migrate
- **Built into Python** - No external dependencies

### When to Upgrade
- If we need high concurrency (many simultaneous writes)
- If we need distributed deployment
- If we need advanced features like replication

## Table Schema

### Users Table

Stores user authentication information.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Unique identifier for each user
- `username` - Unique username for login
- `password_hash` - Hashed password (never store plain text!)
- `created_at` - When the user account was created

**Indexes:**
- Unique index on `username` for fast lookups

### Boards Table

Stores Kanban board data for each user.

```sql
CREATE TABLE boards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    columns_data TEXT NOT NULL,
    cards_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Fields:**
- `id` - Unique identifier for each board
- `user_id` - Foreign key to users table (who owns this board)
- `title` - Board title (e.g., "My Project")
- `columns_data` - JSON string containing column definitions
- `cards_data` - JSON string containing card definitions
- `created_at` - When the board was created
- `updated_at` - When the board was last modified

**Foreign Key:**
- `user_id` references `users(id)`
- `ON DELETE CASCADE` - If user is deleted, their boards are also deleted

**Indexes:**
- Index on `user_id` for fast user-to-boards lookups

## JSON Structure

### columns_data Format

```json
[
  {
    "id": "col-1",
    "title": "Backlog",
    "cardIds": ["card-1", "card-2"]
  },
  {
    "id": "col-2",
    "title": "In Progress",
    "cardIds": ["card-3"]
  }
]
```

**Explanation:**
- Array of column objects
- Each column has: `id`, `title`, `cardIds` (array of card IDs)
- `cardIds` maintains the order of cards in each column

### cards_data Format

```json
{
  "card-1": {
    "id": "card-1",
    "title": "Design homepage",
    "details": "Create mockups and get approval"
  },
  "card-2": {
    "id": "card-2",
    "title": "Setup database",
    "details": "Install SQLite and create tables"
  }
}
```

**Explanation:**
- Object with card IDs as keys
- Each card has: `id`, `title`, `details`
- Using object with IDs as keys allows O(1) lookups

## Why JSON Storage?

### Advantages
- **Flexibility** - Easy to add new fields to cards/columns without schema changes
- **Simplicity** - No need for separate tables for cards and columns
- **Performance** - Single query to get entire board data
- **Matches frontend** - Frontend already uses this structure

### Trade-offs
- **No SQL queries on card data** - Can't query "all cards with title containing X"
- **No foreign key constraints** - Cards aren't in separate table
- **Acceptable for MVP** - We don't need complex queries on card data

## Relationships

```
users (1) ----< (many) boards
```

- Each user can have multiple boards
- Each board belongs to exactly one user
- One-to-many relationship via `user_id` foreign key

## Database Initialization

The database will be created automatically on first run:
1. Check if database file exists
2. If not, create it
3. Create tables with the schema above
4. Ready to use

## Security Considerations

### Password Hashing
- Never store plain text passwords
- Use bcrypt or similar hashing algorithm
- Hashing is one-way (can't reverse to get password)
- We'll implement this in Part 6

### SQL Injection Prevention
- Use parameterized queries (SQLAlchemy handles this)
- Never concatenate user input into SQL strings
- SQLAlchemy ORM provides protection by default

## Future Schema Extensions

If we need to add features later, we can:
- Add new columns to existing tables (ALTER TABLE)
- Add new tables (e.g., for shared boards, comments)
- Extend JSON structure for cards/columns

## Example Data Flow

1. User logs in with username/password
2. Query `users` table to verify credentials
3. Query `boards` table for user's boards
4. Parse `columns_data` and `cards_data` JSON
5. Display board in frontend
6. When user makes changes:
   - Update JSON in memory
   - Serialize back to JSON strings
   - Update `boards` table with new JSON
   - Update `updated_at` timestamp
