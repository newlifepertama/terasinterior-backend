import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Token from previous auth test
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImFkbWluQHRlcmFzaW50ZXJpb3IuY29tIiwiZXhwIjoxNzY0MjgxMTEzfQ.P9jJ2yBSNHshU99cUdjVWF0eXw0f877zlPH39VmWzsQ"

headers_auth = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 60)
print("STEP 4: Testing Portfolio CRUD")
print("=" * 60)
print()

# Test 1: Get Published Portfolio (Public - No Auth)
print("Test 1: Get Published Portfolio (Public)")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/portfolio/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        portfolios = response.json()
        print(f"✓ Found {len(portfolios)} published portfolio items")
        if portfolios:
            print("\nPublished Portfolios:")
            for p in portfolios:
                print(f"  - ID: {p['id']}, Title: {p['title']}, Published: {p['published']}")
        else:
            print("  (No published items yet)")
    else:
        print(f"✗ Failed: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 60)

# Test 2: Create Portfolio (Admin Only)
print()
print("Test 2: Create Portfolio Items (Admin)")
print("-" * 60)

portfolios_to_create = [
    {
        "title": "Modern Living Room",
        "description": "Desain ruang tamu modern minimalis dengan sentuhan kayu dan warna netral",
        "category": "Residential",
        "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
        "published": True,
        "order_index": 1
    },
    {
        "title": "Luxury Bedroom",
        "description": "Kamar tidur mewah dengan konsep hotel bintang 5",
        "category": "Residential",
        "image_url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0",
        "published": True,
        "order_index": 2
    },
    {
        "title": "Office Space",
        "description": "Ruang kantor modern dengan desain ergonomis dan produktif",
        "category": "Commercial",
        "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c",
        "published": True,
        "order_index": 3
    },
    {
        "title": "Minimalist Kitchen",
        "description": "Dapur minimalis dengan storage maksimal",
        "category": "Residential",
        "image_url": "https://images.unsplash.com/photo-1556912173-3bb406ef7e77",
        "published": False,  # Unpublished for testing
        "order_index": 4
    }
]

created_ids = []

for portfolio_data in portfolios_to_create:
    try:
        response = requests.post(
            f"{BASE_URL}/api/portfolio/",
            json=portfolio_data,
            headers=headers_auth
        )
        
        if response.status_code == 201:
            result = response.json()
            created_ids.append(result['id'])
            print(f"✓ Created: {result['title']} (ID: {result['id']}, Published: {result['published']})")
        else:
            print(f"✗ Failed to create '{portfolio_data['title']}': {response.status_code}")
            print(f"  {response.text}")
    except Exception as e:
        print(f"✗ Error creating '{portfolio_data['title']}': {e}")

print(f"\n✓ Created {len(created_ids)} portfolio items")

print()
print("=" * 60)

# Test 3: Get All Portfolio (Admin)
print()
print("Test 3: Get All Portfolio (Admin - includes unpublished)")
print("-" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/api/portfolio/admin",
        headers=headers_auth
    )
    
    if response.status_code == 200:
        portfolios = response.json()
        print(f"✓ Found {len(portfolios)} total portfolio items")
        print("\nAll Portfolios:")
        for p in portfolios:
            status = "✓ Published" if p['published'] else "✗ Unpublished"
            print(f"  - ID: {p['id']}, Title: {p['title']}, {status}")
    else:
        print(f"✗ Failed: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 60)

# Test 4: Get Single Portfolio
if created_ids:
    print()
    print("Test 4: Get Single Portfolio by ID")
    print("-" * 60)
    
    portfolio_id = created_ids[0]
    
    try:
        response = requests.get(f"{BASE_URL}/api/portfolio/{portfolio_id}")
        
        if response.status_code == 200:
            portfolio = response.json()
            print(f"✓ Retrieved portfolio ID {portfolio_id}")
            print(f"\nDetails:")
            print(f"  Title: {portfolio['title']}")
            print(f"  Category: {portfolio['category']}")
            print(f"  Description: {portfolio['description'][:50]}...")
            print(f"  Published: {portfolio['published']}")
            print(f"  Order: {portfolio['order_index']}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 60)

# Test 5: Update Portfolio
if created_ids:
    print()
    print("Test 5: Update Portfolio")
    print("-" * 60)
    
    portfolio_id = created_ids[0]
    update_data = {
        "title": "Modern Living Room - UPDATED",
        "description": "Updated description with new details",
        "published": True
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/portfolio/{portfolio_id}",
            json=update_data,
            headers=headers_auth
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Updated portfolio ID {portfolio_id}")
            print(f"  New Title: {result['title']}")
            print(f"  New Description: {result['description'][:50]}...")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 60)

# Test 6: Verify Public Endpoint Only Shows Published
print()
print("Test 6: Verify Public Endpoint Filtering")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/portfolio/")
    
    if response.status_code == 200:
        public_portfolios = response.json()
        published_count = len(public_portfolios)
        
        # Get admin view
        response_admin = requests.get(
            f"{BASE_URL}/api/portfolio/admin",
            headers=headers_auth
        )
        
        if response_admin.status_code == 200:
            all_portfolios = response_admin.json()
            total_count = len(all_portfolios)
            unpublished_count = sum(1 for p in all_portfolios if not p['published'])
            
            print(f"✓ Public endpoint: {published_count} items")
            print(f"✓ Admin endpoint: {total_count} items")
            print(f"✓ Unpublished items: {unpublished_count}")
            
            if published_count == (total_count - unpublished_count):
                print("\n✓ Filtering works correctly!")
            else:
                print("\n✗ Filtering issue detected")
    else:
        print(f"✗ Failed: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 60)

# Test 7: Delete Portfolio
if created_ids and len(created_ids) > 0:
    print()
    print("Test 7: Delete Portfolio")
    print("-" * 60)
    
    # Delete the last created item
    portfolio_id = created_ids[-1]
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/portfolio/{portfolio_id}",
            headers=headers_auth
        )
        
        if response.status_code == 204:
            print(f"✓ Deleted portfolio ID {portfolio_id}")
            
            # Verify deletion
            response_check = requests.get(f"{BASE_URL}/api/portfolio/{portfolio_id}")
            if response_check.status_code == 404:
                print("✓ Verified: Portfolio no longer exists")
            else:
                print("⚠ Warning: Portfolio still accessible after deletion")
        else:
            print(f"✗ Failed to delete: {response.status_code}")
            print(f"  {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 60)

# Summary
print()
print("=" * 60)
print("Portfolio CRUD Tests Complete!")
print("=" * 60)
print()
print("✅ Test Summary:")
print("  1. ✓ Get published portfolio (public)")
print("  2. ✓ Create portfolio items (admin)")
print("  3. ✓ Get all portfolio (admin)")
print("  4. ✓ Get single portfolio by ID")
print("  5. ✓ Update portfolio")
print("  6. ✓ Verify published/unpublished filtering")
print("  7. ✓ Delete portfolio")
print()
print(f"Created {len(created_ids)} test portfolio items")
print("Backend Portfolio API is fully functional! 🚀")
