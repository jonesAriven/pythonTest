/*
operate_type = args[0]  # Moved Created Deleted Modified ,这里的moved指的是重命名，而不是移动
        file_type = args[1]  # file directory
        src_name = args[2]  # file or directory name
        des_src_name = ""
*/
-- mysql创建存储过程与oracle不同，oracle是create or replace,mysql 是先drop producer if exists,再create
DROP PROCEDURE IF EXISTS `p_window_explore_log`;

CREATE PROCEDURE `p_window_explore_log` (
	IN i_operate_type VARCHAR (32),
	IN i_file_type VARCHAR (32),
	IN i_src_name VARCHAR (1024),
	IN i_des_src_name VARCHAR (1024),
	IN i_current_st_mtime VARCHAR (256)
) NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER COMMENT ''
BEGIN

IF i_src_name REGEXP '.doc$' OR i_des_src_name REGEXP '.doc$' AND i_file_type = 'file' THEN
	INSERT INTO t_window_doc_update (updateTime,file_path,des_file_path,operateType,fileType,ext1)
  VALUES (SYSDATE(),i_src_name,i_des_src_name,i_operate_type,i_file_type,'0');
END IF;

INSERT INTO t_window_explore_update_log (updateTime,file_path,des_file_path,operateType,fileType)
VALUES(SYSDATE(),i_src_name,i_des_src_name,i_operate_type,i_file_type);

-- mysql 判读是直接用"="号，而不是"==",需额外注意
IF i_file_type = 'file' THEN
  IF i_operate_type = 'Moved' THEN
    UPDATE t_window_explore_file SET full_fileName = i_des_src_name WHERE current_st_mtime = i_current_st_mtime;
  ELSEIF i_operate_type = 'Created' THEN
    INSERT INTO t_window_explore_file (full_fileName,current_st_mtime,updateTime)
    VALUES(i_src_name,i_current_st_mtime,SYSDATE());
  ELSEIF i_operate_type = 'Deleted' THEN
    DELETE FROM t_window_explore_file WHERE full_fileName = i_src_name;
  ELSE
    UPDATE t_window_explore_file SET current_st_mtime = i_current_st_mtime WHERE full_fileName = i_src_name;
  END IF;
END IF;

COMMIT;

END;