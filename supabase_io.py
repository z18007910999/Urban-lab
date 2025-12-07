# supabase_io.py
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE"]  # 后端安全环境

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 表名
ARTICLES_TABLE = "News_storage"   # 你的源表（图里这张）
REVIEWS_TABLE  = "news_reviews"   # 目标表（自定义，下面有建表示例）

# 读取字段（与你表结构一致）
ARTICLE_FIELDS = ["id","title","creator","link","pubdate","summary","row_no","Publisher","Category"]

def fetch_articles(limit: int = 200) -> List[Dict[str, Any]]:
    """读取 News_storage 最新文章"""
    res = (supabase.table(ARTICLES_TABLE)
           .select(",".join(ARTICLE_FIELDS))
           .order("pubdate", desc=True)
           .limit(limit)
           .execute())
    return res.data or []

def fetch_article_by_id(article_id: int | str) -> Optional[Dict[str, Any]]:
    res = (supabase.table(ARTICLES_TABLE)
           .select(",".join(ARTICLE_FIELDS))
           .eq("id", article_id)
           .limit(1)
           .execute())
    rows = res.data or []
    return rows[0] if rows else None

def upsert_review(review_row: Dict[str, Any]) -> Dict[str, Any]:
    """
    写入/更新一条审核结果。要求 REVIEWS_TABLE 上 id 唯一（primary key 或 unique），
    这样 upsert(on_conflict="id") 可以覆盖同一篇的最新审核。
    """
    if not isinstance(review_row.get("reviewed_at", None), str):
        review_row["reviewed_at"] = datetime.utcnow().isoformat() + "Z"

    res = supabase.table(REVIEWS_TABLE).upsert(review_row, on_conflict="id").execute()
    return (res.data or [{}])[0]
