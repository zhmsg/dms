set @module_no=26;
delete from predefine_param where api_no in (select api_no from api_info where module_no=@module_no);
delete from api_example where api_no in (select api_no from api_info where module_no=@module_no);
delete from api_params where api_no in (select api_no from api_info where module_no=@module_no);
delete from api_care where api_no in (select api_no from api_info where module_no=@module_no);
delete from api_header where api_no in (select api_no from api_info where module_no=@module_no);
delete from api_info where module_no=@module_no;
delete from api_module where module_no=@module_no;
delete from module_care where module_no=@module_no;
