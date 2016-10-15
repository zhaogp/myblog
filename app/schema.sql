drop table if exists blog;
create table blog(
	id integer primary key autoincrement,
	title text not null,
	content text not null
);
insert into blog(title, content) values('sam card', 'for one month');
