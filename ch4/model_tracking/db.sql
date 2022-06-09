drop table if exists model_track;
drop table if exists model_metric;
drop table if exists model_params;
drop table if exists model_task;

create table model_task
(
	task_id integer PRIMARY KEY ASC,
	task_name text not null,
	task_description text,
	tracked_time text default CURRENT_TIMESTAMP not null,
	del_flag integer default 0 not null
);
create table model_metric
(
	metric_id integer PRIMARY KEY ASC,
	model_id integer not null,
	metric_name text not null,
	metric_type text not null,
	epoch integer not null,
	metric_value float not null,
    is_best integer default 0 not null,
	tracked_time text default CURRENT_TIMESTAMP not null
);

create table model_track
(
	model_id integer PRIMARY KEY ASC,
	task_id integer not null,
	model_sequence integer not null,
	model_name text not null,
	model_description text,
	tracked_time text default CURRENT_TIMESTAMP not null,
	del_flag integer default 0 not null
);

create table model_params
(
	param_id integer PRIMARY KEY ASC,
	model_id integer not null,
	param_type text not null,
	param_name text not null,
	param_value text not null,
	tracked_time text default CURRENT_TIMESTAMP not null
);
