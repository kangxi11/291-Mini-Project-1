import sqlite3


def main():
    conn = sqlite3.connect("mp1.db")
    c = conn.cursor()

    c.executescript(""" 
                    drop table if exists demeritNotices;
                    drop table if exists tickets;
                    drop table if exists registrations;
                    drop table if exists vehicles;
                    drop table if exists marriages;
                    drop table if exists births;
                    drop table if exists persons;
                    drop table if exists payments;
                    drop table if exists users;""")

    conn.commit()

    c.execute("PRAGMA foreign_keys = ON;")

    conn.commit()

    c.executescript("""create table persons (
  fname		char(12),
  lname		char(12),
  bdate		date,
  bplace	char(20),
  address	char(30),
  phone		char(12),
  primary key (fname, lname)
);
create table births (
  regno		int,
  fname		char(12),
  lname		char(12),
  regdate	date,
  regplace	char(20),
  gender	char(1),
  f_fname	char(12),
  f_lname	char(12),
  m_fname	char(12),
  m_lname	char(12),
  primary key (regno),
  foreign key (fname,lname) references persons,
  foreign key (f_fname,f_lname) references persons,
  foreign key (m_fname,m_lname) references persons
);
create table marriages (
  regno		int,
  regdate	date,
  regplace	char(20),
  p1_fname	char(12),
  p1_lname	char(12),
  p2_fname	char(12),
  p2_lname	char(12),
  primary key (regno),
  foreign key (p1_fname,p1_lname) references persons,
  foreign key (p2_fname,p2_lname) references persons
);
create table vehicles (
  vin		char(5),
  make		char(10),
  model		char(10),
  year		int,
  color		char(10),
  primary key (vin)
);
create table registrations (
  regno		int,
  regdate	date,
  expiry	date,
  plate		char(7),
  vin		char(5),
  fname		char(12),
  lname		char(12),
  primary key (regno),
  foreign key (vin) references vehicles,
  foreign key (fname,lname) references persons
);
create table tickets (
  tno		int,
  regno		int,
  fine		int,
  violation	text,
  vdate		date,
  primary key (tno),
  foreign key (regno) references registrations
);
create table demeritNotices (
  ddate		date,
  fname		char(12),
  lname		char(12),
  points	int,
  desc		text,
  primary key (ddate,fname,lname),
  foreign key (fname,lname) references persons
);
create table payments (
  tno		int,
  pdate		date,
  amount	int,
  primary key (tno, pdate),
  foreign key (tno) references tickets
);
create table users (
  uid		char(8),
  pwd		char(8),
  utype		char(1),	-- 'a' for agents, 'o' for officers
  fname		char(12),
  lname		char(12),
  city		char(15),
  primary key(uid),
  foreign key (fname,lname) references persons
);
  

    """)

    conn.commit()





    c.executescript("""insert into persons values ('Michael','Fox','1961-06-09','Edmonton, AB','Manhattan, New York, US', '212-111-1111');
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


insert into vehicles values ('U200', 'Chevrolet', 'Camaro', 1969, 'red');
insert into vehicles values ('U201', 'Toyoto', 'Corolla', 2012, 'red');
insert into vehicles values ('U202', 'Toyoto', 'RAV4', 2013, 'red');
insert into vehicles values ('U203', 'Kia', 'Cube', 2013, 'red');

insert into vehicles values ('U300', 'Mercedes', 'SL 230', 1964, 'black');
insert into vehicles values ('U301', 'Audi', 'A4', 2013, 'black');
insert into vehicles values ('U302', 'Toyoto', 'RAV4', 2012, 'black');
insert into vehicles values ('U400', 'Chevrolet', 'Camaro', 2012, 'black');


insert into vehicles values ('U500', 'Chevrolet', 'Camaro', 1969, 'white');
insert into vehicles values ('U501', 'Audi', 'A4', 2012, 'white');
insert into vehicles values ('U502', 'Chevrolet', 'Camaro', 2012, 'white');
insert into vehicles values ('U505', 'Audi', 'A4', 2013, 'white');
insert into vehicles values ('U506', 'Audi', 'A4', 2014, 'white');
insert into vehicles values ('U508', 'Audi', 'A4', 2016, 'white');
insert into vehicles values ('U509', 'Audi', 'A4', 2014, 'white');




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

insert into users values ('101', '12345', 'a', 'John', 'Truyens', 'Edmonton');
insert into users values ('102', 'password', 'o', 'Horace', 'Combs', 'Edmonton');

    """)

    conn.commit()

main()