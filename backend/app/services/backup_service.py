import os
import datetime
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any

from app.core.database import engine

class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self) -> Dict[str, Any]:
        """创建数据库备份"""
        try:
            print("开始创建数据库备份...")
            
            # 获取数据库连接信息
            db_url = str(engine.url)
            print(f"数据库URL: {db_url}")
            
            # 生成备份文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.sql"
            backup_path = self.backup_dir / backup_filename
            print(f"备份文件路径: {backup_path}")
            
            # 使用pg_dump创建备份（PostgreSQL）
            if db_url.startswith("postgresql"):
                print("使用pg_dump创建PostgreSQL备份...")
                # 解析PostgreSQL连接字符串
                from urllib.parse import urlparse
                parsed_url = urlparse(db_url)
                
                db_name = parsed_url.path[1:]  # 移除开头的斜杠
                print(f"数据库名称: {db_name}")
                
                cmd = [
                    "pg_dump",
                    "-h", parsed_url.hostname or "localhost",
                    "-p", str(parsed_url.port or 5432),
                    "-U", parsed_url.username or "postgres",
                    "-d", db_name,
                    "-f", str(backup_path),
                    "--no-password"
                ]
                
                print(f"备份命令: {' '.join(cmd)}")
                
                # 设置环境变量避免密码提示
                env = os.environ.copy()
                if parsed_url.password:
                    env["PGPASSWORD"] = parsed_url.password
                    print("已设置PGPASSWORD环境变量")
                
                try:
                    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
                    print(f"备份命令执行成功，输出: {result.stdout}")
                except subprocess.CalledProcessError as e:
                    print(f"备份命令执行失败，错误: {e.stderr}")
                    raise
            
            # 使用sqlite3创建备份（SQLite）
            elif db_url.startswith("sqlite"):
                print("使用sqlite3创建SQLite备份...")
                db_path = db_url.replace("sqlite:///", "")
                cmd = [
                    "sqlite3",
                    db_path,
                    f".backup {backup_path}"
                ]
                subprocess.run(cmd, check=True)
            
            # 获取备份文件信息
            backup_size = backup_path.stat().st_size
            print(f"备份文件大小: {backup_size} 字节")
            
            return {
                "success": True,
                "filename": backup_filename,
                "path": str(backup_path),
                "size": backup_size,
                "timestamp": timestamp
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"备份命令执行失败: {e.stderr if e.stderr else str(e)}"
            print(f"错误: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
        except FileNotFoundError:
            error_msg = "备份工具未找到，请确保已安装pg_dump或sqlite3命令行工具"
            print(f"错误: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"备份创建失败: {str(e)}"
            print(f"错误: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    def get_backup_list(self) -> List[Dict[str, Any]]:
        """获取备份文件列表"""
        backups = []
        
        try:
            for file in sorted(self.backup_dir.glob("backup_*.sql"), reverse=True):
                stat = file.stat()
                backups.append({
                    "filename": file.name,
                    "path": str(file),
                    "size": stat.st_size,
                    "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
            
            return backups
            
        except Exception as e:
            return []
    
    def download_backup(self, filename: str) -> str:
        """获取备份文件路径"""
        backup_path = self.backup_dir / filename
        
        if backup_path.exists():
            return str(backup_path)
        return None
    
    def restore_backup(self, filename: str) -> Dict[str, Any]:
        """恢复备份"""
        try:
            backup_path = self.backup_dir / filename
            
            if not backup_path.exists():
                return {"success": False, "error": "备份文件不存在"}
            
            # 获取数据库连接信息
            db_url = str(engine.url)
            
            # 使用psql恢复备份（PostgreSQL）
            if db_url.startswith("postgresql"):
                cmd = [
                    "psql",
                    "-d", db_url,
                    "-f", str(backup_path)
                ]
                subprocess.run(cmd, check=True)
            
            # 使用sqlite3恢复备份（SQLite）
            elif db_url.startswith("sqlite"):
                db_path = db_url.replace("sqlite:///", "")
                # 先备份当前数据库
                temp_backup = f"temp_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite"
                shutil.copy2(db_path, temp_backup)
                
                # 恢复备份
                cmd = [
                    "sqlite3",
                    db_path,
                    f".read {backup_path}"
                ]
                subprocess.run(cmd, check=True)
                
                # 删除临时备份
                if os.path.exists(temp_backup):
                    os.remove(temp_backup)
            
            return {"success": True}
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup_old_backups(self, keep_count: int = 7) -> Dict[str, Any]:
        """清理旧备份，保留指定数量的最新备份"""
        try:
            backups = sorted(self.backup_dir.glob("backup_*.sql"), key=lambda x: x.stat().st_ctime, reverse=True)
            
            if len(backups) > keep_count:
                old_backups = backups[keep_count:]
                deleted_count = 0
                
                for backup in old_backups:
                    backup.unlink()
                    deleted_count += 1
                
                return {    
                    "success": True,
                    "deleted_count": deleted_count
                }
            
            return {"success": True, "deleted_count": 0}
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

backup_service = BackupService()