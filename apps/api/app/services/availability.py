from datetime import datetime, timedelta
from app.models import ShelterStatus


def apply_conservatism_rule(status: ShelterStatus) -> None:
    """
    Apply conservatism rule: downgrade to UNKNOWN after 12 hours
    """
    if not status.last_updated:
        return
    
    # Check if more than 12 hours have passed
    if datetime.utcnow() - status.last_updated > timedelta(hours=12):
        if status.status in ['OPEN', 'LIMITED']:
            status.status = 'UNKNOWN'
            # Note: We don't update last_updated here to preserve the original timestamp


def should_send_notification(prev_status: ShelterStatus, new_status: ShelterStatus) -> bool:
    """
    Determine if a notification should be sent when status changes
    """
    # Send notification when beds become available (0 -> >0)
    if (prev_status.beds_available == 0 and 
        new_status.beds_available > 0 and
        new_status.status in ['OPEN', 'LIMITED']):
        return True
    
    return False


def calculate_availability_percentage(status: ShelterStatus) -> float:
    """
    Calculate availability percentage
    """
    if status.beds_total == 0:
        return 0.0
    
    return (status.beds_available / status.beds_total) * 100


def get_status_from_availability(beds_available: int, beds_total: int) -> str:
    """
    Determine status based on availability
    """
    if beds_available == 0:
        return 'FULL'
    elif beds_available <= beds_total * 0.25:
        return 'LIMITED'
    else:
        return 'OPEN'
