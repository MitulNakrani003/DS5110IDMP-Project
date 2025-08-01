import pymysql
import json
from config import DatabaseConfig

class MBTAAssistant:

    def __init__(self):
        self.connection = pymysql.connect(
            host=DatabaseConfig.DB_HOST,
            port=int(DatabaseConfig.DB_PORT),
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD,
            database=DatabaseConfig.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = self.connection.cursor()
        
        cursor.execute("""
            SELECT name, id
            FROM mbta_lines 
            WHERE is_active = 1
        """)
        all_lines = cursor.fetchall()
        lines_id_dict = {line['name']: line['id'] for line in all_lines}

        line_to_stops = {}
        for line_name, line_id in lines_id_dict.items():
            cursor.execute("""
                SELECT s.name AS stops
                FROM line_stops AS ls
                JOIN stops AS s ON ls.stop_id = s.id
                WHERE ls.line_id = %s AND is_active = 1
            """, (line_id,))
            stops = cursor.fetchall()
            stops = [stop['stops'] for stop in stops]
            line_to_stops[line_name] = stops
        
        green_branches = {}
        green_branches['B'] = line_to_stops['Green Line B']
        green_branches['C'] = line_to_stops['Green Line C']
        green_branches['D'] = line_to_stops['Green Line D']
        green_branches['E'] = line_to_stops['Green Line E']

        self.lines = {
            'red': {'name': 'Red Line', 'stations': line_to_stops['Red Line']},
            'orange': {'name': 'Orange Line', 'stations': line_to_stops['Orange Line']},
            'blue': {'name': 'Blue Line', 'stations': line_to_stops['Blue Line']},
            'green': {
                'name': 'Green Line',
                'branches': green_branches
            }
        }
        print(self.lines)
        
        # Define transfer stations
        self.transfer_stations = {
            'Park Street': ['red', 'green'],#
            'Downtown Crossing': ['red', 'orange'],#
            'State': ['orange', 'blue'],#
            'Government Center': ['blue', 'green'],#
            'Haymarket': ['orange', 'green'],
            'North Station': ['orange', 'green'],#
            'Copley': ['green'],
            'Arlington': ['green'],
            'Boylston': ['green']
        }
        
    
    
    def find_station_line(self, station_name):
        """Find which line(s) a station belongs to"""
        station_name = station_name.lower().strip()
        lines_found = []
        
        # Check regular lines
        for line, info in self.lines.items():
            if line == 'green':
                # Check Green Line branches
                for branch, stations in info['branches'].items():
                    if any(station.lower() == station_name for station in stations):
                        lines_found.append(f'green-{branch}')
            else:
                if any(station.lower() == station_name for station in info['stations']):
                    lines_found.append(line)
        
        return lines_found
    
    def get_route(self, start_station, end_station):
        """Get route between two stations"""
        start = start_station.strip()
        end = end_station.strip()
        
        # Find lines for both stations
        start_lines = self.find_station_line(start)
        end_lines = self.find_station_line(end)
        
        if not start_lines:
            return f"Station '{start}' not found in the MBTA system."
        if not end_lines:
            return f"Station '{end}' not found in the MBTA system."
        
        # Check if they're on the same line
        for start_line in start_lines:
            for end_line in end_lines:
                if start_line.split('-')[0] == end_line.split('-')[0]:  # Same line (handling green branches)
                    return self._get_direct_route(start, end, start_line.split('-')[0])
        
        # If not on same line, find transfer route
        return self._get_transfer_route(start, end, start_lines, end_lines)
    
    def _get_direct_route(self, start, end, line):
        """Get route when both stations are on the same line"""
        if line == 'green':
            # For Green Line, check which branch(es) contain both stations
            for branch, stations in self.lines['green']['branches'].items():
                start_idx = None
                end_idx = None
                for i, station in enumerate(stations):
                    if station.lower() == start.lower():
                        start_idx = i
                    if station.lower() == end.lower():
                        end_idx = i
                
                if start_idx is not None and end_idx is not None:
                    direction = "outbound" if end_idx > start_idx else "inbound"
                    stops = abs(end_idx - start_idx)
                    return f"Take Green Line ({branch} branch) {direction} from {start} to {end}. ({stops} stops)"
        else:
            # For other lines
            stations = self.lines[line]['stations']
            start_idx = None
            end_idx = None
            for i, station in enumerate(stations):
                if station.lower() == start.lower():
                    start_idx = i
                if station.lower() == end.lower():
                    end_idx = i
            
            if start_idx is not None and end_idx is not None:
                direction = "outbound" if end_idx > start_idx else "inbound"
                stops = abs(end_idx - start_idx)
                return f"Take {self.lines[line]['name']} {direction} from {start} to {end}. ({stops} stops)"
        
        return "Route not found."
    
    def _get_transfer_route(self, start, end, start_lines, end_lines):
        """Find route requiring transfer"""
        # Simple implementation: find common transfer stations
        for transfer_station, lines in self.transfer_stations.items():
            # Check if we can reach transfer station from start
            can_reach_from_start = False
            for start_line in start_lines:
                if start_line.split('-')[0] in lines:
                    can_reach_from_start = True
                    start_to_transfer_line = start_line.split('-')[0]
                    break
            
            # Check if we can reach end from transfer station
            can_reach_end = False
            for end_line in end_lines:
                if end_line.split('-')[0] in lines:
                    can_reach_end = True
                    transfer_to_end_line = end_line.split('-')[0]
                    break
            
            if can_reach_from_start and can_reach_end and start_to_transfer_line != transfer_to_end_line:
                return (f"Take {self.lines[start_to_transfer_line]['name']} from {start} to {transfer_station}, "
                       f"then transfer to {self.lines[transfer_to_end_line]['name']} to {end}.")
        
        return "No direct route found. Multiple transfers (2+) may be required."
    
    def get_line_info(self, line_name):
        """Get information about a specific line"""
        line_name = line_name.lower().strip()
        
        if line_name in self.lines:
            info = self.lines[line_name]
            if line_name == 'green':
                response = f"{info['name']} has 4 branches (B, C, D, E):\n"
                for branch, stations in info['branches'].items():
                    response += f"\n{branch} Branch: {len(stations)} stations from {stations[0]} to {stations[-1]}"
                return response
            else:
                stations = info['stations']
                return f"{info['name']} has {len(stations)} stations from {stations[0]} to {stations[-1]}."
        else:
            return f"Line '{line_name}' not found. Available lines: Red, Orange, Blue, Green."
    
    def answer_question(self, question):
        """Main function to answer MBTA-related questions"""
        question = question.lower()
        
        # Route queries
        if 'from' in question and 'to' in question:
            # Extract station names
            parts = question.split('from')
            if len(parts) > 1:
                remaining = parts[1].split('to')
                if len(remaining) > 1:
                    start = remaining[0].strip()
                    end = remaining[1].strip().rstrip('?.')
                    return self.get_route(start, end)
        
        # Line information queries
        elif any(line in question for line in ['red line', 'orange line', 'blue line', 'green line']):
            for line in ['red', 'orange', 'blue', 'green']:
                if f'{line} line' in question:
                    return self.get_line_info(line)
        
        # Station lookup
        elif 'which line' in question or 'what line' in question:
            # Extract station name
            words = question.split()
            # Try to find quoted station name or station name before/after keywords
            station_name = None
            if '"' in question:
                start = question.find('"') + 1
                end = question.find('"', start)
                if end > start:
                    station_name = question[start:end]
            else:
                # Simple extraction - look for station name after 'is'
                if ' is ' in question:
                    parts = question.split(' is ')
                    if len(parts) > 1:
                        station_name = parts[1].strip().rstrip('?. on')
            
            if station_name:
                lines = self.find_station_line(station_name)
                if lines:
                    if len(lines) == 1:
                        return f"{station_name.title()} is on the {lines[0].replace('-', ' ').title()}."
                    else:
                        return f"{station_name.title()} is on the following lines: {', '.join(lines)}."
                else:
                    return f"Station '{station_name}' not found in the MBTA system."
        
        return "I can help with MBTA routes and station information. Try asking:\n" \
               "- 'How do I get from Harvard to South Station?'\n" \
               "- 'Which line is Park Street on?'\n" \
               "- 'Tell me about the Red Line'"


# Example usage
# if __name__ == "__main__":
#     assistant = MBTAAssistant()
#     # Test queries
#     print(assistant.answer_question("How do I get from Harvard to South Station?"))
#     print("\n" + assistant.answer_question("Which line is Park Street on?"))
#     print("\n" + assistant.answer_question("Tell me about the Red Line"))
#     print("\n" + assistant.answer_question("How do I get from Assembly to Riverside?"))
#     print("\n" + assistant.get_route("Harvard", "Stony Brook"))
#     print("\n" + assistant.answer_question("What line is Copley on?"))
#     print("\n" + assistant.answer_question("How to get from Davis to Airport?"))