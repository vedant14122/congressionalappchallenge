#!/usr/bin/env python3
"""
Seed script for ShelterLink database
Populates with LA County shelters and resources
"""

import asyncio
import sys
import os
from decimal import Decimal
from datetime import time
from uuid import uuid4

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import AsyncSessionLocal, engine
from app.models import Shelter, ShelterStatus, Resource, Staff, TranslationString


async def create_shelters():
    """Create sample shelters across LA neighborhoods"""
    
    shelters_data = [
        {
            "name": "Downtown Women's Center",
            "address": "442 S San Pedro St, Los Angeles, CA 90013",
            "lat": Decimal("34.0456"),
            "lon": Decimal("-118.2456"),
            "neighborhood": "Skid Row",
            "phone": "(213) 680-0600",
            "hours": "24/7",
            "website": "https://www.downtownwomenscenter.org",
            "requires_id": True,
            "pet_friendly": False,
            "ada_accessible": True,
            "lgbtq_friendly": True,
            "curfew_time": time(22, 0),
            "intake_notes": "Women only. Photo ID required. Call ahead for availability.",
            "languages": ["en", "es"]
        },
        {
            "name": "Union Rescue Mission",
            "address": "545 S San Pedro St, Los Angeles, CA 90013",
            "lat": Decimal("34.0445"),
            "lon": Decimal("-118.2445"),
            "neighborhood": "Skid Row",
            "phone": "(213) 347-6300",
            "hours": "24/7",
            "website": "https://urm.org",
            "requires_id": False,
            "pet_friendly": True,
            "ada_accessible": True,
            "lgbtq_friendly": True,
            "curfew_time": time(21, 0),
            "intake_notes": "All genders welcome. Pets allowed. No ID required.",
            "languages": ["en", "es", "ko"]
        },
        {
            "name": "Koreatown Youth & Community Center",
            "address": "3727 W 6th St, Los Angeles, CA 90020",
            "lat": Decimal("34.0654"),
            "lon": Decimal("-118.3045"),
            "neighborhood": "Koreatown",
            "phone": "(213) 365-7400",
            "hours": "8:00 AM - 8:00 PM",
            "website": "https://kyccla.org",
            "requires_id": False,
            "pet_friendly": False,
            "ada_accessible": True,
            "lgbtq_friendly": True,
            "curfew_time": time(20, 0),
            "intake_notes": "Youth-focused services. Korean language support available.",
            "languages": ["en", "ko", "es"]
        },
        {
            "name": "Hollywood Homeless Youth Partnership",
            "address": "1541 N Cahuenga Blvd, Los Angeles, CA 90028",
            "lat": Decimal("34.1023"),
            "lon": Decimal("-118.3245"),
            "neighborhood": "Hollywood",
            "phone": "(323) 462-4013",
            "hours": "9:00 AM - 6:00 PM",
            "website": "https://hhyp.org",
            "requires_id": False,
            "pet_friendly": True,
            "ada_accessible": True,
            "lgbtq_friendly": True,
            "curfew_time": None,
            "intake_notes": "Youth services. LGBTQ+ friendly. Drop-in center.",
            "languages": ["en", "es"]
        },
        {
            "name": "Venice Family Clinic",
            "address": "604 Rose Ave, Venice, CA 90291",
            "lat": Decimal("33.9987"),
            "lon": Decimal("-118.4567"),
            "neighborhood": "Venice",
            "phone": "(310) 392-8636",
            "hours": "8:00 AM - 5:00 PM",
            "website": "https://venicefamilyclinic.org",
            "requires_id": False,
            "pet_friendly": False,
            "ada_accessible": True,
            "lgbtq_friendly": True,
            "curfew_time": None,
            "intake_notes": "Healthcare services. No shelter beds, but can refer to housing.",
            "languages": ["en", "es"]
        }
    ]
    
    shelters = []
    for data in shelters_data:
        shelter = Shelter(
            id=uuid4(),
            **data
        )
        shelters.append(shelter)
    
    return shelters


async def create_shelter_statuses(shelters):
    """Create status entries for shelters"""
    
    statuses = []
    
    # Downtown Women's Center - Women only
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[0].id,
        category="WOMEN",
        beds_total=50,
        beds_available=12,
        status="LIMITED",
        notes="Limited availability. Call ahead."
    ))
    
    # Union Rescue Mission - Mixed
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[1].id,
        category="MIXED",
        beds_total=100,
        beds_available=45,
        status="OPEN",
        notes="Good availability. Pet-friendly."
    ))
    
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[1].id,
        category="MEN",
        beds_total=60,
        beds_available=25,
        status="OPEN",
        notes="Men's section available."
    ))
    
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[1].id,
        category="WOMEN",
        beds_total=40,
        beds_available=20,
        status="OPEN",
        notes="Women's section available."
    ))
    
    # Koreatown Youth Center - Youth
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[2].id,
        category="YOUTH",
        beds_total=20,
        beds_available=8,
        status="LIMITED",
        notes="Youth services. Korean language support."
    ))
    
    # Hollywood Youth Partnership - Youth
    statuses.append(ShelterStatus(
        id=uuid4(),
        shelter_id=shelters[3].id,
        category="YOUTH",
        beds_total=15,
        beds_available=0,
        status="FULL",
        notes="Currently full. Check back daily."
    ))
    
    return statuses


async def create_resources():
    """Create sample resources across LA"""
    
    resources_data = [
        {
            "name": "LA Mission Food Bank",
            "type": "FOOD",
            "address": "303 E 5th St, Los Angeles, CA 90013",
            "lat": Decimal("34.0445"),
            "lon": Decimal("-118.2445"),
            "neighborhood": "Skid Row",
            "hours": "8:00 AM - 4:00 PM",
            "phone": "(213) 629-1227",
            "notes": "Free meals daily. No ID required."
        },
        {
            "name": "Mobile Shower Program - Venice",
            "type": "SHOWER",
            "address": "Windward Circle, Venice, CA 90291",
            "lat": Decimal("33.9987"),
            "lon": Decimal("-118.4567"),
            "neighborhood": "Venice",
            "hours": "9:00 AM - 3:00 PM, Tue/Thu/Sat",
            "phone": "(310) 392-8636",
            "notes": "Mobile shower unit. Towels and hygiene supplies provided."
        },
        {
            "name": "Koreatown Cooling Center",
            "type": "COOLING",
            "address": "3727 W 6th St, Los Angeles, CA 90020",
            "lat": Decimal("34.0654"),
            "lon": Decimal("-118.3045"),
            "neighborhood": "Koreatown",
            "hours": "10:00 AM - 6:00 PM (during heat waves)",
            "phone": "(213) 365-7400",
            "notes": "Air-conditioned space during extreme heat."
        },
        {
            "name": "Safe Parking LA - Hollywood",
            "type": "SAFE_PARKING",
            "address": "1541 N Cahuenga Blvd, Los Angeles, CA 90028",
            "lat": Decimal("34.1023"),
            "lon": Decimal("-118.3245"),
            "neighborhood": "Hollywood",
            "hours": "6:00 PM - 7:00 AM",
            "phone": "(323) 462-4013",
            "notes": "Overnight parking for people living in vehicles. Security provided."
        },
        {
            "name": "LA County Health Services",
            "type": "HEALTH",
            "address": "313 N Figueroa St, Los Angeles, CA 90012",
            "lat": Decimal("34.0556"),
            "lon": Decimal("-118.2445"),
            "neighborhood": "Downtown LA",
            "hours": "8:00 AM - 5:00 PM",
            "phone": "(213) 240-8000",
            "notes": "Medical services. Sliding scale fees."
        }
    ]
    
    resources = []
    for data in resources_data:
        resource = Resource(
            id=uuid4(),
            **data
        )
        resources.append(resource)
    
    return resources


async def create_staff():
    """Create sample staff members"""
    
    staff_data = [
        {
            "email": "admin@shelterlink.org",
            "shelter_id": None,
            "role": "ADMIN",
            "locale": "en"
        },
        {
            "email": "staff@downtownwomenscenter.org",
            "shelter_id": None,  # Will be set after shelter creation
            "role": "STAFF",
            "locale": "en"
        }
    ]
    
    staff = []
    for data in staff_data:
        staff_member = Staff(
            id=uuid4(),
            **data
        )
        staff.append(staff_member)
    
    return staff


async def create_translations():
    """Create sample translation strings"""
    
    translations = [
        # English
        {"key": "shelter.requires_id", "lang": "en", "value": "Photo ID Required"},
        {"key": "shelter.pet_friendly", "lang": "en", "value": "Pet Friendly"},
        {"key": "shelter.ada_accessible", "lang": "en", "value": "ADA Accessible"},
        {"key": "shelter.lgbtq_friendly", "lang": "en", "value": "LGBTQ+ Friendly"},
        {"key": "status.open", "lang": "en", "value": "Open"},
        {"key": "status.limited", "lang": "en", "value": "Limited"},
        {"key": "status.full", "lang": "en", "value": "Full"},
        {"key": "status.unknown", "lang": "en", "value": "Unknown"},
        
        # Spanish
        {"key": "shelter.requires_id", "lang": "es", "value": "Se Requiere Identificación"},
        {"key": "shelter.pet_friendly", "lang": "es", "value": "Acepta Mascotas"},
        {"key": "shelter.ada_accessible", "lang": "es", "value": "Accesible para Discapacitados"},
        {"key": "shelter.lgbtq_friendly", "lang": "es", "value": "Amigable con LGBTQ+"},
        {"key": "status.open", "lang": "es", "value": "Abierto"},
        {"key": "status.limited", "lang": "es", "value": "Limitado"},
        {"key": "status.full", "lang": "es", "value": "Lleno"},
        {"key": "status.unknown", "lang": "es", "value": "Desconocido"},
        
        # Korean
        {"key": "shelter.requires_id", "lang": "ko", "value": "신분증 필요"},
        {"key": "shelter.pet_friendly", "lang": "ko", "value": "반려동물 허용"},
        {"key": "shelter.ada_accessible", "lang": "ko", "value": "장애인 접근 가능"},
        {"key": "shelter.lgbtq_friendly", "lang": "ko", "value": "LGBTQ+ 친화적"},
        {"key": "status.open", "lang": "ko", "value": "개방"},
        {"key": "status.limited", "lang": "ko", "value": "제한적"},
        {"key": "status.full", "lang": "ko", "value": "만원"},
        {"key": "status.unknown", "lang": "ko", "value": "알 수 없음"},
    ]
    
    translation_objects = []
    for data in translations:
        translation = TranslationString(
            id=uuid4(),
            **data
        )
        translation_objects.append(translation)
    
    return translation_objects


async def main():
    """Main seeding function"""
    
    print("🌱 Starting ShelterLink database seeding...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Create shelters
            print("Creating shelters...")
            shelters = await create_shelters()
            session.add_all(shelters)
            await session.commit()
            
            # Create shelter statuses
            print("Creating shelter statuses...")
            statuses = await create_shelter_statuses(shelters)
            session.add_all(statuses)
            await session.commit()
            
            # Create resources
            print("Creating resources...")
            resources = await create_resources()
            session.add_all(resources)
            await session.commit()
            
            # Create staff
            print("Creating staff...")
            staff = await create_staff()
            session.add_all(staff)
            await session.commit()
            
            # Create translations
            print("Creating translations...")
            translations = await create_translations()
            session.add_all(translations)
            await session.commit()
            
            print("✅ Database seeding completed successfully!")
            print(f"Created {len(shelters)} shelters, {len(statuses)} statuses, {len(resources)} resources, {len(staff)} staff, {len(translations)} translations")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
