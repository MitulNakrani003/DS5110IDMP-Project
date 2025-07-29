from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import json
from config import DatabaseConfig

app = FastAPI(title="MBTA System API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Create database connection using PyMySQL"""
    try:
        connection = pymysql.connect(
            host=DatabaseConfig.DB_HOST,
            port=int(DatabaseConfig.DB_PORT),
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD,
            database=DatabaseConfig.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/")
async def root():
    """Home endpoint with database connection test and MBTA map information"""
    try:
        connection = get_db_connection()
        if not connection:
            return {
                "message": "MBTA System API",
                "version": "1.0.0",
                "database_status": "error",
                "error": "Could not connect to database",
                "mbta_map": {
                    "map_url": "https://cdn.mbta.com/sites/default/files/2022-12/2022-12-12-subway-map-v37f.pdf",
                    "interactive_map": "https://www.mbta.com/schedules/subway",
                    "last_updated": "2024-01-01"
                }
            }
        
        with connection.cursor() as cursor:
            # Get total lines
            cursor.execute("SELECT COUNT(*) as count FROM mbta_lines")
            total_lines = cursor.fetchone()['count']
            
            # Get total stations
            cursor.execute("SELECT COUNT(*) as count FROM stops")
            total_stations = cursor.fetchone()['count']
            
            # Get total fares
            cursor.execute("SELECT COUNT(*) as count FROM fares")
            total_fares = cursor.fetchone()['count']
        
        connection.close()
        
        return {
            "message": "MBTA System API",
            "version": "1.0.0",
            "database_status": "connected",
            "stats": {
                "total_lines": total_lines,
                "total_stations": total_stations,
                "total_fares": total_fares
            },
            "mbta_map": {
                "map_url": "https://cdn.mbta.com/sites/default/files/2022-12/2022-12-12-subway-map-v37f.pdf",
                "interactive_map": "https://www.mbta.com/schedules/subway",
                "last_updated": "2024-01-01"
            }
        }
    except Exception as e:
        return {
            "message": "MBTA System API",
            "version": "1.0.0",
            "database_status": "error",
            "error": str(e),
            "mbta_map": {
                "map_url": "https://cdn.mbta.com/sites/default/files/2022-12/2022-12-12-subway-map-v37f.pdf",
                "interactive_map": "https://www.mbta.com/schedules/subway",
                "last_updated": "2024-01-01"
            }
        }

@app.get("/api/lines")
async def get_lines():
    """Get all MBTA lines"""
    try:
        connection = get_db_connection()
        if not connection:
            return {"error": "Database connection failed"}
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, color, code, is_active 
                FROM mbta_lines 
                WHERE is_active = 1
            """)
            lines = cursor.fetchall()
            
            # Get station count for each line
            for line in lines:
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM line_stops 
                    WHERE line_id = %s
                """, (line['id'],))
                line['station_count'] = cursor.fetchone()['count']
        
        connection.close()
        return {"lines": lines, "total_count": len(lines)}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/stations")
async def get_stations():
    """Get all stations"""
    try:
        connection = get_db_connection()
        if not connection:
            return {"error": "Database connection failed"}
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, stop_code, is_active 
                FROM stops 
                WHERE is_active = 1
            """)
            stations = cursor.fetchall()
        
        connection.close()
        return {"stations": stations, "total_count": len(stations)}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/stations/{line_name}")
async def get_stations_by_line(line_name: str):
    """Get stations by line name"""
    try:
        connection = get_db_connection()
        if not connection:
            return {"error": "Database connection failed"}
        
        with connection.cursor() as cursor:
            # Get line info
            cursor.execute("""
                SELECT id, name, color, code 
                FROM mbta_lines 
                WHERE name LIKE %s AND is_active = 1
            """, (f"%{line_name}%",))
            line = cursor.fetchone()
            
            if not line:
                return {"error": f"Line '{line_name}' not found"}
            
            # Get stations for this line
            cursor.execute("""
                SELECT s.id, s.name, s.stop_code, ls.stop_sequence, ls.is_terminal
                FROM line_stops ls
                JOIN stops s ON ls.stop_id = s.id
                WHERE ls.line_id = %s AND s.is_active = 1
                ORDER BY ls.stop_sequence
            """, (line['id'],))
            stations = cursor.fetchall()
        
        connection.close()
        
        return {
            "line": line,
            "stations": stations,
            "count": len(stations)
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)