from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(prefix="/api/stats", tags=["Statistics"])

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        # Portfolio stats
        portfolio_result = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN published THEN 1 ELSE 0 END) as published FROM portfolio"))
        portfolio_stats = portfolio_result.fetchone()
        
        # Services stats
        services_result = db.execute(text("SELECT COUNT(*) as total FROM services"))
        services_stats = services_result.fetchone()
        
        # Contacts stats
        contacts_result = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new FROM contacts"))
        contacts_stats = contacts_result.fetchone()
        
        # Recent activity
        recent_portfolio = db.execute(text("SELECT id, title, created_at FROM portfolio ORDER BY created_at DESC LIMIT 3"))
        recent_contacts = db.execute(text("SELECT id, name, created_at FROM contacts ORDER BY created_at DESC LIMIT 3"))
        
        activities = []
        for row in recent_portfolio:
            activities.append({
                "id": row.id,
                "type": "portfolio",
                "action": "created",
                "title": row.title,
                "timestamp": row.created_at.isoformat()
            })
        
        for row in recent_contacts:
            activities.append({
                "id": row.id,
                "type": "contact",
                "action": "created",
                "title": f"Pesan dari {row.name}",
                "timestamp": row.created_at.isoformat()
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "totalPortfolio": portfolio_stats.total or 0,
            "publishedPortfolio": portfolio_stats.published or 0,
            "totalServices": services_stats.total or 0,
            "totalContacts": contacts_stats.total or 0,
            "newContacts": contacts_stats.new or 0,
            "recentActivity": activities[:5]
        }
    except Exception as e:
        print(f"Dashboard stats error: {e}")
        return {
            "totalPortfolio": 0,
            "publishedPortfolio": 0,
            "totalServices": 0,
            "totalContacts": 0,
            "newContacts": 0,
            "recentActivity": []
        }

@router.get("/contact-trend")
async def get_contact_trend(db: Session = Depends(get_db)):
    """Get contact submissions by month (last 6 months)"""
    try:
        result = db.execute(text("""
            SELECT 
                TO_CHAR(created_at, 'Mon YYYY') as month,
                COUNT(*) as count
            FROM contacts
            WHERE created_at >= NOW() - INTERVAL '6 months'
            GROUP BY TO_CHAR(created_at, 'Mon YYYY'), DATE_TRUNC('month', created_at)
            ORDER BY DATE_TRUNC('month', created_at)
        """))
        
        return [{"month": row.month, "count": row.count} for row in result]
    except Exception as e:
        print(f"Contact trend error: {e}")
        return []
