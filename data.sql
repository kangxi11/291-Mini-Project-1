-- Data prepared by Ryan Kang, rkang1@ualberta.ca
-- Published on Oct 4, 2019
-- Modified Oct 10, 2019

-- Compatible with initial data published on Sept 26, 2019
-- By Dr. Davood Rafiei
insert into persons values ('Michael','Fox','1961-06-09','Edmonton, AB','Manhattan, New York, US', '212-111-1111');
insert into persons values ('Walt', 'Disney', '1901-12-05', 'Chicago, US', 'Los Angeles, US', '213-555-5555');
insert into persons values ('Lillian', 'Bounds', '1899-02-15', 'Spalding, Idaho', 'Los Angeles, US', '213-555-5556');
insert into persons values ('John', 'Truyens', '1907-05-15', 'Flanders, Belgium', 'Beverly Hills, Los Angeles, US', '213-555-5558');
insert into persons values ('Mickey', 'Mouse', '1928-01-05', 'Disneyland, FL', 'Anaheim, US', '714-555-5551');
insert into persons values ('Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'Anaheim, US', '714-555-5551');
insert into persons values ('Amalia', 'Kane', '1928-07-03', 'Marvin Plains, OK', 'Toronto, ON', '534-529-7567');
insert into persons values ('Horace', 'Combs', '1965-10-02', 'Anaheim, US', 'Anaheim, US', '500-986-3991');
insert into persons values ('Wendy', 'Ballard', '1953-05-15', 'Halifax, NS', 'Fort McMurray, AB', '203-347-1629');
insert into persons values ('Stacey', 'Long', '1953-05-15', 'Halifax, NS', 'Fort McMurray, AB', '203-347-1629');
insert into persons values ('Mia', 'Warner', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');
insert into persons values ('Davood','Rafiei',date('now','-21 years'),'Iran','100 Lovely Street,Edmonton,AB', '780-111-2222');
insert into persons values ('Throw', 'Away', '1944-12-25', 'St John, NB', 'Toronto, ON', '661-578-1287');



insert into births values (100,'Mickey', 'Mouse', '1928-02-05', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into births values (200,'Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'F', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into births values (300,'Michael', 'Fox', '1961-06-09', 'Edmonton, AB', 'M', 'John', 'Truyens', 'Amalia', 'Kane');
insert into births values (700,'Michael', 'Fox', '1961-06-09', 'Edmonton, AB', 'M', NULL, NULL, 'Amalia', 'Kane');



insert into marriages values (200, '1925-07-13', 'Idaho, US', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into marriages values (201, '1969-05-03', 'Los Angeles, US', 'Lillian', 'Bounds', 'John', 'Truyens');


insert into vehicles values ('U200', 'Chevrolet', 'Camaro', 2012, 'red');
insert into vehicles values ('U201', 'Toyoto', 'Corolla', 2012, 'red');
insert into vehicles values ('U202', 'Toyoto', 'RAV4', 2012, 'red');
insert into vehicles values ('U203', 'Kia', 'Cube', 2012, 'red');

insert into vehicles values ('U300', 'Mercedes', 'SL 230', 2012, 'black');
insert into vehicles values ('U301', 'Audi', 'A4', 2012, 'black');
insert into vehicles values ('U302', 'Toyoto', 'RAV4', 2012, 'black');
insert into vehicles values ('U400', 'Chevrolet', 'Camaro', 2012, 'black');


insert into vehicles values ('U500', 'Chevrolet', 'Camaro', 1969, 'white');
insert into vehicles values ('U501', 'Audi', 'A4', 2012, 'white');
insert into vehicles values ('U502', 'Chevrolet', 'Camaro', 2012, 'white');
insert into vehicles values ('U505', 'Audi', 'A4', 2013, 'white');
insert into vehicles values ('U506', 'Audi', 'A4', 2014, 'white');
insert into vehicles values ('U508', 'Audi', 'A4', 2016, 'white');
insert into vehicles values ('U509', 'Audi', 'A4', 2000, 'white');




insert into registrations values (300, '1964-05-26','1965-05-25', 'DISNEY','U300', 'Walt', 'Disney');
insert into registrations values (302, '1980-01-16','1981-01-15', 'LILLI','U200', 'Lillian', 'Bounds');
insert into registrations values (301, '1981-06-26','2020-07-15', 'M7F8J2','U400', 'Wendy', 'Ballard');
insert into registrations values (303, '1991-01-26','2007-07-25', 'Z7F9J2','U500', 'Davood', 'Rafiei');
insert into registrations values (304, '2012-01-26','2020-07-25', 'Z7F9J2','U201', 'John', 'Truyens');
insert into registrations values (305, '2013-01-26','2021-07-25', 'Z7F9J2','U202', 'Minnie', 'Mouse');
insert into registrations values (306, '1913-01-26','2018-07-25', 'Z7F9J2','U203', 'Amalia', 'Kane');
insert into registrations values (307, '2013-01-26','2020-07-25', 'Z7F9J2','U301', 'Amalia', 'Kane');
insert into registrations values (308, '2012-01-26','2001-07-25', 'Z7F9J2','U302', 'Horace', 'Combs');
insert into registrations values (311, '2012-01-26','2008-07-25', 'Z7F9J2','U501', 'Horace', 'Combs');
insert into registrations values (309, '2012-01-26','2030-07-25', 'Z7F9J2','U502', 'Davood', 'Rafiei');
insert into registrations values (310, '2013-01-26','2021-07-25', 'Z7F9J2','U505', 'Stacey', 'Long');
insert into registrations values (314, '2019-03-26','2041-07-25', 'Z7F9J2','U508', 'Davood', 'Rafiei');
insert into registrations values (315, '2019-04-26','2025-07-25', 'Z7F9J2','U509', 'Davood', 'Rafiei');
insert into registrations values (317, '2019-03-26','2025-06-25', 'Z7F9J2','U509', 'Davood', 'Rafiei');
insert into registrations values (318, '2019-04-26','2025-07-25', 'Z7F9J2', 'U509', 'Davood', 'Rafiei');
insert into registrations values (319, '2019-08-26','2025-08-25', 'Z7F9J2', 'U509', 'Davood', 'Rafiei');



insert into tickets values (400,300,4,'speeding','1964-08-20');
insert into tickets values (401,302,10,'speeding','2019-08-20');
insert into tickets values (402,304,10,'speeding','2018-08-20');
insert into tickets values (403,305,15,'speeding','2019-08-20');
insert into tickets values (404,306,30,'speeding','2017-08-20');
insert into tickets values (405,307,30,'speeding','2019-09-21');
insert into tickets values (406,305,20,'speeding','2019-01-20');
insert into tickets values (407,305,60,'speeding','2019-04-20');
insert into tickets values (414,314,12,'passed in red light of calgary','2019-05-20');
insert into tickets values (415,315,14,'speeding','2019-06-20');
insert into tickets values (416,315,15,'dasin rEd lIght VIOLATION','2019-07-20');


insert into demeritNotices values ('1964-08-20', 'Walt', 'Disney', 2, 'Speeding');


insert into payments values (400, '2019-09-21', 5);
insert into payments values (407, '2019-09-21', 15);

insert into users values (101, '12345', 'a', 'John', 'Truyens', 'Edmonton');
insert into users values (102, 'password', 'o', 'Horace', 'Combs', 'Edmonton');
insert into users values ('user1', 'abcd', 'a', 'Mia', 'Warner', 'Toronto');
