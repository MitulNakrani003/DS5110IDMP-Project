USE SmartTransitApp;

-- Insert MBTA subway lines
INSERT INTO mbta_lines (name, color, code, is_active) VALUES
('Red Line', 'Red', 'RL', 1),
('Orange Line', 'Orange', 'OL', 1),
('Blue Line', 'Blue', 'BL', 1),
('Green Line B', 'Green', 'GLB', 1),
('Green Line C', 'Green', 'GLC', 1),
('Green Line D', 'Green', 'GLD', 1),
('Green Line E', 'Green', 'GLE', 1);

-- Insert unique MBTA subway stops
INSERT INTO stops (name, stop_code, is_active) VALUES
('Alewife', 'ALEWF', 1),
('Davis', 'DAVIS', 1),
('Porter', 'PORTR', 1),
('Harvard', 'HARSQ', 1),
('Central', 'CENTR', 1),
('Kendall/MIT', 'KNDLE', 1),
('Charles/MGH', 'CHMNL', 1),
('Park Street', 'PKSTR', 1),
('Downtown Crossing', 'DWNXG', 1),
('South Station', 'SSTAT', 1),
('Broadway', 'BRDWY', 1),
('Andrew', 'ANDRW', 1),
('JFK/UMass', 'JFKUM', 1),
('Savin Hill', 'SAVHL', 1),
('Fields Corner', 'FLDCR', 1),
('Shawmut', 'SHMNR', 1),
('Ashmont', 'ASHMN', 1),
('North Quincy', 'NQNCY', 1),
('Wollaston', 'WLSTA', 1),
('Quincy Center', 'QNCTR', 1),
('Quincy Adams', 'QADMS', 1),
('Braintree', 'BRNTR', 1),
('Oak Grove', 'OAKGR', 1),
('Malden Center', 'MALDL', 1),
('Wellington', 'WELLN', 1),
('Assembly', 'ASMBL', 1),
('Sullivan Square', 'SLLVN', 1),
('Community College', 'CCOLL', 1),
('North Station', 'NSTAT', 1),
('Haymarket', 'HAYMK', 1),
('State', 'STATE', 1),
('Chinatown', 'CHNTW', 1),
('Tufts Medical Center', 'TUFTS', 1),
('Back Bay', 'BBSTA', 1),
('Massachusetts Avenue', 'MASS', 1),
('Ruggles', 'RUGG', 1),
('Roxbury Crossing', 'ROXBY', 1),
('Jackson Square', 'JAKSN', 1),
('Stony Brook', 'SBRK', 1),
('Green Street', 'GRNST', 1),
('Forest Hills', 'FORHL', 1),
('Wonderland', 'WONDL', 1),
('Revere Beach', 'REVBH', 1),
('Beachmont', 'BCHMT', 1),
('Suffolk Downs', 'SUFDN', 1),
('Orient Heights', 'ORHTE', 1),
('Wood Island', 'WDLND', 1),
('Airport', 'AIRPT', 1),
('Maverick', 'MVRIK', 1),
('Aquarium', 'AQURM', 1),
('Government Center', 'GOVER', 1),
('Bowdoin', 'BOWDN', 1),
('Boylston', 'BOYLS', 1),
('Arlington', 'ARLIG', 1),
('Copley', 'COPLY', 1),
('Hynes Convention Center', 'HYNES', 1),
('Kenmore', 'KENMR', 1),
('Blandford Street', 'BLAND', 1),
('Boston University East', 'BUE', 1),
('Boston University Central', 'BUC', 1),
('Boston University West', 'BUW', 1),
('Saint Paul Street', 'STPUL', 1),
('Pleasant Street', 'PLSNT', 1),
('Babcock Street', 'BABCK', 1),
('Packards Corner', 'PACKD', 1),
('Harvard Avenue', 'HVDAV', 1),
('Griggs Street', 'GRIGG', 1),
('Allston Street', 'ALLST', 1),
('Warren Street', 'WARRN', 1),
('Washington Street', 'WSHST', 1),
('Sutherland Road', 'STHLD', 1),
('Chiswick Road', 'CHSWK', 1),
('Chestnut Hill Avenue', 'CHILL', 1),
('South Street', 'STHST', 1),
('Boston College', 'BCOLL', 1),
('Cleveland Circle', 'CLMNL', 1),
('Englewood Avenue', 'ENGWD', 1),
('Dean Road', 'DEAN', 1),
('Tappan Street', 'TAPPN', 1),
('Washington Square', 'WSHSQ', 1),
('Fairbanks Street', 'FAIRB', 1),
('Brandon Hall', 'BRNHL', 1),
('Summit Avenue', 'SUMMR', 1),
('Coolidge Corner', 'COECN', 1),
('Kent Street', 'KENT', 1),
('Saint Marys Street', 'SMARY', 1),
('Hawes Street', 'HAWES', 1),
('Riverside', 'RIVER', 1),
('Woodland', 'WDLND2', 1),
('Waban', 'WABAN', 1),
('Eliot', 'ELIOT', 1),
('Newton Centre', 'NEWCN', 1),
('Newton Highlands', 'NEWHI', 1),
('Chestnut Hill', 'CHSTL', 1),
('Reservoir', 'RESER', 1),
('Beaconsfield', 'BCNSF', 1),
('Brookline Hills', 'BRKHL', 1),
('Brookline Village', 'BRKVL', 1),
('Longwood Medical Area', 'LONGW', 1),
('Fenway', 'FENWY', 1),
('Heath Street', 'HEATH', 1),
('Back of the Hill', 'BACKH', 1),
('Riverway', 'RIVWY', 1),
('Mission Park', 'MISPK', 1),
('Fenwood Road', 'FENWD', 1),
('Brigham Circle', 'BRGHM', 1),
('Museum of Fine Arts', 'MFA', 1),
('Northeastern University', 'NORTU', 1),
('Symphony', 'SYMPH', 1),
('Prudential', 'PRUDE', 1),
('Lechmere', 'LCHME', 1),
('Science Park', 'SCPAK', 1),
('Union Square', 'UNION', 1),
('East Somerville', 'ESOMV', 1),
('Gilman Square', 'GILMN', 1),
('Magoun Square', 'MAGOU', 1),
('Ball Square', 'BALLS', 1),
('Medford/Tufts', 'MEDFD', 1);


-- Insert Red Line stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
-- Red Line (Alewife to Ashmont/Braintree)
(1, (SELECT id FROM stops WHERE name = 'Alewife'), 1, 1),
(1, (SELECT id FROM stops WHERE name = 'Davis'), 2, 0),
(1, (SELECT id FROM stops WHERE name = 'Porter'), 3, 0),
(1, (SELECT id FROM stops WHERE name = 'Harvard'), 4, 0),
(1, (SELECT id FROM stops WHERE name = 'Central'), 5, 0),
(1, (SELECT id FROM stops WHERE name = 'Kendall/MIT'), 6, 0),
(1, (SELECT id FROM stops WHERE name = 'Charles/MGH'), 7, 0),
(1, (SELECT id FROM stops WHERE name = 'Park Street'), 8, 0),
(1, (SELECT id FROM stops WHERE name = 'Downtown Crossing'), 9, 0),
(1, (SELECT id FROM stops WHERE name = 'South Station'), 10, 0),
(1, (SELECT id FROM stops WHERE name = 'Broadway'), 11, 0),
(1, (SELECT id FROM stops WHERE name = 'Andrew'), 12, 0),
(1, (SELECT id FROM stops WHERE name = 'JFK/UMass'), 13, 0),
-- Ashmont Branch
(1, (SELECT id FROM stops WHERE name = 'Savin Hill'), 14, 0),
(1, (SELECT id FROM stops WHERE name = 'Fields Corner'), 15, 0),
(1, (SELECT id FROM stops WHERE name = 'Shawmut'), 16, 0),
(1, (SELECT id FROM stops WHERE name = 'Ashmont'), 17, 1),
-- Braintree Branch
(1, (SELECT id FROM stops WHERE name = 'North Quincy'), 14, 0),
(1, (SELECT id FROM stops WHERE name = 'Wollaston'), 15, 0),
(1, (SELECT id FROM stops WHERE name = 'Quincy Center'), 16, 0),
(1, (SELECT id FROM stops WHERE name = 'Quincy Adams'), 17, 0),
(1, (SELECT id FROM stops WHERE name = 'Braintree'), 18, 1);

-- Insert Orange Line stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(2, (SELECT id FROM stops WHERE name = 'Oak Grove'), 1, 1),
(2, (SELECT id FROM stops WHERE name = 'Malden Center'), 2, 0),
(2, (SELECT id FROM stops WHERE name = 'Wellington'), 3, 0),
(2, (SELECT id FROM stops WHERE name = 'Assembly'), 4, 0),
(2, (SELECT id FROM stops WHERE name = 'Sullivan Square'), 5, 0),
(2, (SELECT id FROM stops WHERE name = 'Community College'), 6, 0),
(2, (SELECT id FROM stops WHERE name = 'North Station'), 7, 0),
(2, (SELECT id FROM stops WHERE name = 'Haymarket'), 8, 0),
(2, (SELECT id FROM stops WHERE name = 'State'), 9, 0),
(2, (SELECT id FROM stops WHERE name = 'Downtown Crossing'), 10, 0),
(2, (SELECT id FROM stops WHERE name = 'Chinatown'), 11, 0),
(2, (SELECT id FROM stops WHERE name = 'Tufts Medical Center'), 12, 0),
(2, (SELECT id FROM stops WHERE name = 'Back Bay'), 13, 0),
(2, (SELECT id FROM stops WHERE name = 'Massachusetts Avenue'), 14, 0),
(2, (SELECT id FROM stops WHERE name = 'Ruggles'), 15, 0),
(2, (SELECT id FROM stops WHERE name = 'Roxbury Crossing'), 16, 0),
(2, (SELECT id FROM stops WHERE name = 'Jackson Square'), 17, 0),
(2, (SELECT id FROM stops WHERE name = 'Stony Brook'), 18, 0),
(2, (SELECT id FROM stops WHERE name = 'Green Street'), 19, 0),
(2, (SELECT id FROM stops WHERE name = 'Forest Hills'), 20, 1);

-- Insert Blue Line stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(3, (SELECT id FROM stops WHERE name = 'Wonderland'), 1, 1),
(3, (SELECT id FROM stops WHERE name = 'Revere Beach'), 2, 0),
(3, (SELECT id FROM stops WHERE name = 'Beachmont'), 3, 0),
(3, (SELECT id FROM stops WHERE name = 'Suffolk Downs'), 4, 0),
(3, (SELECT id FROM stops WHERE name = 'Orient Heights'), 5, 0),
(3, (SELECT id FROM stops WHERE name = 'Wood Island'), 6, 0),
(3, (SELECT id FROM stops WHERE name = 'Airport'), 7, 0),
(3, (SELECT id FROM stops WHERE name = 'Maverick'), 8, 0),
(3, (SELECT id FROM stops WHERE name = 'Aquarium'), 9, 0),
(3, (SELECT id FROM stops WHERE name = 'State'), 10, 0),
(3, (SELECT id FROM stops WHERE name = 'Government Center'), 11, 0),
(3, (SELECT id FROM stops WHERE name = 'Bowdoin'), 12, 1);

-- Insert Green Line B Branch stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(4, (SELECT id FROM stops WHERE name = 'Government Center'), 1, 0),
(4, (SELECT id FROM stops WHERE name = 'Park Street'), 2, 0),
(4, (SELECT id FROM stops WHERE name = 'Boylston'), 3, 0),
(4, (SELECT id FROM stops WHERE name = 'Arlington'), 4, 0),
(4, (SELECT id FROM stops WHERE name = 'Copley'), 5, 0),
(4, (SELECT id FROM stops WHERE name = 'Hynes Convention Center'), 6, 0),
(4, (SELECT id FROM stops WHERE name = 'Kenmore'), 7, 0),
(4, (SELECT id FROM stops WHERE name = 'Blandford Street'), 8, 0),
(4, (SELECT id FROM stops WHERE name = 'Boston University East'), 9, 0),
(4, (SELECT id FROM stops WHERE name = 'Boston University Central'), 10, 0),
(4, (SELECT id FROM stops WHERE name = 'Boston University West'), 11, 0),
(4, (SELECT id FROM stops WHERE name = 'Saint Paul Street'), 12, 0),
(4, (SELECT id FROM stops WHERE name = 'Pleasant Street'), 13, 0),
(4, (SELECT id FROM stops WHERE name = 'Babcock Street'), 14, 0),
(4, (SELECT id FROM stops WHERE name = 'Packards Corner'), 15, 0),
(4, (SELECT id FROM stops WHERE name = 'Harvard Avenue'), 16, 0),
(4, (SELECT id FROM stops WHERE name = 'Griggs Street'), 17, 0),
(4, (SELECT id FROM stops WHERE name = 'Allston Street'), 18, 0),
(4, (SELECT id FROM stops WHERE name = 'Warren Street'), 19, 0),
(4, (SELECT id FROM stops WHERE name = 'Washington Street'), 20, 0),
(4, (SELECT id FROM stops WHERE name = 'Sutherland Road'), 21, 0),
(4, (SELECT id FROM stops WHERE name = 'Chiswick Road'), 22, 0),
(4, (SELECT id FROM stops WHERE name = 'Chestnut Hill Avenue'), 23, 0),
(4, (SELECT id FROM stops WHERE name = 'South Street'), 24, 0),
(4, (SELECT id FROM stops WHERE name = 'Boston College'), 25, 1);

-- Insert Green Line C Branch stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(5, (SELECT id FROM stops WHERE name = 'North Station'), 1, 0),
(5, (SELECT id FROM stops WHERE name = 'Haymarket'), 2, 0),
(5, (SELECT id FROM stops WHERE name = 'Government Center'), 3, 0),
(5, (SELECT id FROM stops WHERE name = 'Park Street'), 4, 0),
(5, (SELECT id FROM stops WHERE name = 'Boylston'), 5, 0),
(5, (SELECT id FROM stops WHERE name = 'Arlington'), 6, 0),
(5, (SELECT id FROM stops WHERE name = 'Copley'), 7, 0),
(5, (SELECT id FROM stops WHERE name = 'Hynes Convention Center'), 8, 0),
(5, (SELECT id FROM stops WHERE name = 'Kenmore'), 9, 0),
(5, (SELECT id FROM stops WHERE name = 'Saint Marys Street'), 10, 0),
(5, (SELECT id FROM stops WHERE name = 'Hawes Street'), 11, 0),
(5, (SELECT id FROM stops WHERE name = 'Kent Street'), 12, 0),
(5, (SELECT id FROM stops WHERE name = 'Saint Paul Street'), 13, 0),
(5, (SELECT id FROM stops WHERE name = 'Coolidge Corner'), 14, 0),
(5, (SELECT id FROM stops WHERE name = 'Summit Avenue'), 15, 0),
(5, (SELECT id FROM stops WHERE name = 'Brandon Hall'), 16, 0),
(5, (SELECT id FROM stops WHERE name = 'Fairbanks Street'), 17, 0),
(5, (SELECT id FROM stops WHERE name = 'Washington Square'), 18, 0),
(5, (SELECT id FROM stops WHERE name = 'Tappan Street'), 19, 0),
(5, (SELECT id FROM stops WHERE name = 'Dean Road'), 20, 0),
(5, (SELECT id FROM stops WHERE name = 'Englewood Avenue'), 21, 0),
(5, (SELECT id FROM stops WHERE name = 'Cleveland Circle'), 22, 1);

-- Insert Green Line D Branch stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(6, (SELECT id FROM stops WHERE name = 'Union Square'), 1, 1),
(6, (SELECT id FROM stops WHERE name = 'Lechmere'), 2, 0),
(6, (SELECT id FROM stops WHERE name = 'Science Park'), 3, 0),
(6, (SELECT id FROM stops WHERE name = 'North Station'), 4, 0),
(6, (SELECT id FROM stops WHERE name = 'Haymarket'), 5, 0),
(6, (SELECT id FROM stops WHERE name = 'Government Center'), 6, 0),
(6, (SELECT id FROM stops WHERE name = 'Park Street'), 7, 0),
(6, (SELECT id FROM stops WHERE name = 'Boylston'), 8, 0),
(6, (SELECT id FROM stops WHERE name = 'Arlington'), 9, 0),
(6, (SELECT id FROM stops WHERE name = 'Copley'), 10, 0),
(6, (SELECT id FROM stops WHERE name = 'Hynes Convention Center'), 11, 0),
(6, (SELECT id FROM stops WHERE name = 'Kenmore'), 12, 0),
(6, (SELECT id FROM stops WHERE name = 'Fenway'), 13, 0),
(6, (SELECT id FROM stops WHERE name = 'Longwood Medical Area'), 14, 0),
(6, (SELECT id FROM stops WHERE name = 'Brookline Village'), 15, 0),
(6, (SELECT id FROM stops WHERE name = 'Brookline Hills'), 16, 0),
(6, (SELECT id FROM stops WHERE name = 'Beaconsfield'), 17, 0),
(6, (SELECT id FROM stops WHERE name = 'Reservoir'), 18, 0),
(6, (SELECT id FROM stops WHERE name = 'Chestnut Hill'), 19, 0),
(6, (SELECT id FROM stops WHERE name = 'Newton Highlands'), 20, 0),
(6, (SELECT id FROM stops WHERE name = 'Newton Centre'), 21, 0),
(6, (SELECT id FROM stops WHERE name = 'Eliot'), 22, 0),
(6, (SELECT id FROM stops WHERE name = 'Waban'), 23, 0),
(6, (SELECT id FROM stops WHERE name = 'Woodland'), 24, 0),
(6, (SELECT id FROM stops WHERE name = 'Riverside'), 25, 1);

-- Insert Green Line E Branch stops with sequence
INSERT INTO line_stops (line_id, stop_id, stop_sequence, is_terminal) VALUES
(7, (SELECT id FROM stops WHERE name = 'Medford/Tufts'), 1, 1),
(7, (SELECT id FROM stops WHERE name = 'Ball Square'), 2, 0),
(7, (SELECT id FROM stops WHERE name = 'Magoun Square'), 3, 0),
(7, (SELECT id FROM stops WHERE name = 'Gilman Square'), 4, 0),
(7, (SELECT id FROM stops WHERE name = 'East Somerville'), 5, 0),
(7, (SELECT id FROM stops WHERE name = 'Lechmere'), 6, 0),
(7, (SELECT id FROM stops WHERE name = 'Science Park'), 7, 0),
(7, (SELECT id FROM stops WHERE name = 'North Station'), 8, 0),
(7, (SELECT id FROM stops WHERE name = 'Haymarket'), 9, 0),
(7, (SELECT id FROM stops WHERE name = 'Government Center'), 10, 0),
(7, (SELECT id FROM stops WHERE name = 'Park Street'), 11, 0),
(7, (SELECT id FROM stops WHERE name = 'Boylston'), 12, 0),
(7, (SELECT id FROM stops WHERE name = 'Arlington'), 13, 0),
(7, (SELECT id FROM stops WHERE name = 'Copley'), 14, 0),
(7, (SELECT id FROM stops WHERE name = 'Prudential'), 15, 0),
(7, (SELECT id FROM stops WHERE name = 'Symphony'), 16, 0),
(7, (SELECT id FROM stops WHERE name = 'Northeastern University'), 17, 0),
(7, (SELECT id FROM stops WHERE name = 'Museum of Fine Arts'), 18, 0),
(7, (SELECT id FROM stops WHERE name = 'Longwood Medical Area'), 19, 0),
(7, (SELECT id FROM stops WHERE name = 'Brigham Circle'), 20, 0),
(7, (SELECT id FROM stops WHERE name = 'Fenwood Road'), 21, 0),
(7, (SELECT id FROM stops WHERE name = 'Mission Park'), 22, 0),
(7, (SELECT id FROM stops WHERE name = 'Riverway'), 23, 0),
(7, (SELECT id FROM stops WHERE name = 'Back of the Hill'), 24, 0),
(7, (SELECT id FROM stops WHERE name = 'Heath Street'), 25, 1);

-- Insert current MBTA fares
INSERT INTO fares (fare_amount, fare_type, description) VALUES
(2.40, 'standard', 'Standard subway fare with CharlieCard'),
(1.10, 'reduced', 'Senior/disabled fare with CharlieCard');






-- Insert transfer station data
INSERT INTO station_connections (station_id, line_ids) VALUES
  -- Park Street (Transfers between Red, Green B/C/D/E)
  ((SELECT id FROM stops WHERE name = 'Park Street'), '1,4,5,6,7'),
  
  -- Downtown Crossing (Transfers between Red, Orange Lines)
  ((SELECT id FROM stops WHERE name = 'Downtown Crossing'), '1,2'),
  
  -- North Station (Transfers between Green C/D/E, Orange Lines)
  ((SELECT id FROM stops WHERE name = 'North Station'), '2,5,6,7'),
  
  -- Haymarket (Transfers between Green C/D/E, Orange Lines)
  ((SELECT id FROM stops WHERE name = 'Haymarket'), '2,5,6,7'),
  
  -- Government Center (Transfers between Green C/D/E, Blue Lines)
  ((SELECT id FROM stops WHERE name = 'Government Center'), '3,5,6,7'),
  
  -- State (Transfers between Orange, Blue Lines)
  ((SELECT id FROM stops WHERE name = 'State'), '2,3'),
  
  -- Copley (Green Line B/C/D/E meet)
  ((SELECT id FROM stops WHERE name = 'Copley'), '4,5,6,7'),
  
  -- Kenmore (Green Line B/C/D meet)
  ((SELECT id FROM stops WHERE name = 'Kenmore'), '4,5,6'),
  
  -- Lechmere (Green Line D/E meet at GLX junction)
  ((SELECT id FROM stops WHERE name = 'Lechmere'), '6,7');
