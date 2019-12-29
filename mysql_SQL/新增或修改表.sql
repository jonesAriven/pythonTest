-- 创建t_window_doc_cache_map表
CREATE TABLE `t_window_doc_cache_map` (
  `id` bigint(10) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `updateTime` datetime DEFAULT NULL COMMENT '文件更新时间',
  `file_path` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '源文件路径',
  `doc_cache_path` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '目标文件路径',
  `st_mtime` varchar(32) DEFAULT NULL COMMENT 'file_path的时间戳',
  `ext1` varchar(256) DEFAULT NULL COMMENT '对于doc的变化是否已经处理，1为处理，0为未处理',
  `ext2` varchar(256) DEFAULT NULL COMMENT '扩展字段2',
  `ext3` varchar(256) DEFAULT NULL COMMENT '扩展字段3',
  PRIMARY KEY (`id`),
  UNIQUE KEY `自增主键` (`id`),
  UNIQUE KEY `唯一索引` (`file_path`),
  KEY `时间索引` (`updateTime`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8;

CREATE TABLE `t_window_explore_file` (
  `id` bigint(12) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '自增索引',
  `full_fileName` varchar(1024) DEFAULT NULL COMMENT '文件名全路径',
  `current_st_mtime` varchar(128) DEFAULT NULL COMMENT '文件时间戳',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  `ext1` varchar(256) DEFAULT NULL COMMENT '扩展字段1',
  `ext2` varchar(256) DEFAULT NULL COMMENT '扩展字段2',
  `ext3` varchar(256) DEFAULT NULL COMMENT '扩展字段3',
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `full_fileName` (`full_fileName`),
  KEY `updateTime` (`updateTime`),
  KEY `current_st_mtime` (`current_st_mtime`)
) ENGINE=InnoDB AUTO_INCREMENT=849665 DEFAULT CHARSET=utf8;

CREATE TABLE `t_window_explore_update_log` (
  `id` bigint(10) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  `file_path` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '源文件路径',
  `des_file_path` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '目标文件路径',
  `operateType` varchar(32) DEFAULT NULL COMMENT '操作类型',
  `fileType` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '文件的类型，是文件夹还是文件',
  `ext1` varchar(256) DEFAULT NULL COMMENT '扩展字段1',
  `ext2` varchar(256) DEFAULT NULL COMMENT '扩展字段2',
  `ext3` varchar(256) DEFAULT NULL COMMENT '扩展字段3',
  PRIMARY KEY (`id`),
  UNIQUE KEY `自增主键` (`id`),
  KEY `时间索引` (`updateTime`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;


