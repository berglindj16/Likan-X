create table itemcategorycode(
	itemcode varchar(250),
	description varchar(250),
	PRIMARY KEY (itemcode)
);

create table voruspjald(
	itemno varchar(250),
	itemcode varchar(250) references itemcategorycode(itemcode),
	baseunitofmeasure varchar(250),
	millilitrar float,
	soluflokkur varchar(250),
	vinstyrkur float,
	unitprice float,
	description varchar(250),
	primary key(itemno) 
);


create table receipt (
	receiptno varchar(250),
	posterminalno varchar(250),
	timasetning time,
	dagsetning date,
	primary key(receiptno)
);

create table receiptitems(
	id SERIAL,
	receiptno varchar(250) references receipt(receiptno),
	itemno varchar(250) references voruspjald(itemno),
	quantity int,
	price float,
	netprice float,
	netamount float,
	vatamount float,
	primary key(id)
);

create table budir (
	nafn varchar(250),
	description varchar(250),
	primary key(nafn)
);


create table hilluplass (
	bud varchar(250) references budir(nafn),
	itemno varchar(250) references voruspjald(itemno),
	magn int,
	primary key(bud,itemno)
);

insert into budir (nafn, description) values ('Hafnarfjordur', 'A detailed description on Hafnarfjordur.');

drop table receiptitems;
drop table receipt;
drop table voruspjald;
drop table itemcategorycode;