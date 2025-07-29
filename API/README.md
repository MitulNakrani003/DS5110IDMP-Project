# MBTA System API with MySQL Database

This FastAPI application provides a comprehensive MBTA (Massachusetts Bay Transportation Authority) system API with MySQL database integration.

## Features

- 🚇 **Station Management**: Get all stations or filter by subway line
- 🛤️ **Route Planning**: Plan routes between stations with fare calculation
- 💬 **AI Chat**: Interactive chat system with database logging
- 📊 **System Statistics**: Get comprehensive MBTA system statistics
- 🗺️ **System Map**: Access to MBTA maps and resources

## Database Schema

The application uses the following MySQL tables:

### Stations Table
- `id`: Primary key
- `name`: Station name
- `line`: Subway line (Red, Orange, Blue, Green)
- `latitude`, `longitude`: GPS coordinates
- `wheelchair_accessible`: Accessibility status
- `created_at`, `updated_at`: Timestamps

### Routes Table
- `id`: Primary key
- `origin_station_id`, `destination_station_id`: Foreign keys to stations
- `line`: Subway line
- `direction`: Route direction
- `estimated_time`: Travel time in minutes
- `fare_regular`, `fare_reduced`, `fare_student`: Fare rates
- `transfers`: Number of transfers required

### Route Steps Table
- `id`: Primary key
- `route_id`: Foreign key to routes
- `step_order`: Step sequence
- `line`: Subway line for this step
- `direction`: Direction for this step
- `stops`: Comma-separated list of stops

### Chat History Table
- `id`: Primary key
- `user_prompt`: User's question
- `ai_response`: AI's response
- `created_at`: Timestamp

## Setup Instructions

### 1. Install Dependencies

```bash
pip3 install -r ../req.txt
```

### 2. Configure Database Connection

Run the setup script to configure your MySQL database:

```bash
python3 setup_database.py
```

This will prompt you for:
- Database host (default: localhost)
- Database port (default: 3306)
- Database name (default: mbta_system)
- Database username (default: root)
- Database password

### 3. Manual Configuration (Alternative)

If you prefer to configure manually, update the `config.py` file:

```python
from config import DatabaseConfig

DatabaseConfig.update_connection(
    host="your_host",
    port="your_port", 
    database="your_database_name",
    username="your_username",
    password="your_password"
)
```

### 4. Run the API

```bash
python3 main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Base Endpoint
- `GET /` - API information

### System Map
- `GET /api/system-map` - Get MBTA system map information

### Stations
- `GET /api/stations` - Get all stations
- `GET /api/stations/{line}` - Get stations by line (Red, Orange, Blue, Green)

### Route Planning
- `POST /api/plan-route` - Plan a route between stations
  ```json
  {
    "origin": "Alewife",
    "destination": "Park Street", 
    "fare_type": "regular"
  }
  ```

### AI Chat
- `POST /api/chat` - Chat with AI assistant
  ```json
  {
    "prompt": "What are the operating hours?"
  }
  ```

### Statistics
- `GET /api/stats` - Get system statistics

## Testing the API

### Using curl

```bash
# Get all stations
curl http://localhost:8000/api/stations

# Get Red Line stations
curl http://localhost:8000/api/stations/Red

# Plan a route
curl -X POST http://localhost:8000/api/plan-route \
  -H "Content-Type: application/json" \
  -d '{"origin": "Alewife", "destination": "Park Street", "fare_type": "regular"}'

# Chat with AI
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the operating hours?"}'

# Get system stats
curl http://localhost:8000/api/stats
```

### Using the Streamlit UI

1. Navigate to the UI directory
2. Run: `streamlit run ui.py`
3. Open the web interface at `http://localhost:8501`

## Environment Variables

You can also configure the database using environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=mbta_system
export DB_USER=root
export DB_PASSWORD=your_password
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure MySQL is running and accessible
2. **Authentication Error**: Verify username and password
3. **Database Not Found**: Create the database first: `CREATE DATABASE mbta_system;`
4. **Permission Error**: Ensure the user has proper permissions

### Database Commands

```sql
-- Create database
CREATE DATABASE mbta_system;

-- Grant permissions
GRANT ALL PRIVILEGES ON mbta_system.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;

-- Check tables
USE mbta_system;
SHOW TABLES;
```

## Sample Data

The application automatically populates the database with:
- 50+ MBTA stations across all 4 subway lines
- Sample routes between major stations
- Wheelchair accessibility information
- GPS coordinates for all stations

## Contributing

Feel free to extend the API with additional features like:
- Real-time train tracking
- Service alerts
- Fare payment integration
- User accounts and favorites 