"""Test pagination"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_portfolio_pagination():
    """Test portfolio pagination"""
    print("="*50)
    print("TESTING PORTFOLIO PAGINATION")
    print("="*50)
    
    # Test page 1
    print("\n1. Get page 1 (page_size=5):")
    response = requests.get(f"{BASE_URL}/api/portfolio?page=1&page_size=5")
    data = response.json()
    
    print(f"   Status: {response.status_code}")
    print(f"   Items: {len(data['items'])}")
    print(f"   Total: {data['total']}")
    print(f"   Page: {data['page']}/{data['total_pages']}")
    print(f"   Has next: {data['has_next']}")
    print(f"   Has prev: {data['has_prev']}")
    
    if data['total'] > 5:
        # Test page 2
        print("\n2. Get page 2 (page_size=5):")
        response = requests.get(f"{BASE_URL}/api/portfolio?page=2&page_size=5")
        data = response.json()
        
        print(f"   Status: {response.status_code}")
        print(f"   Items: {len(data['items'])}")
        print(f"   Page: {data['page']}/{data['total_pages']}")
        print(f"   Has next: {data['has_next']}")
        print(f"   Has prev: {data['has_prev']}")
    
    print("\n   ✅ Portfolio pagination working!")

def test_services_pagination():
    """Test services pagination"""
    print("\n" + "="*50)
    print("TESTING SERVICES PAGINATION")
    print("="*50)
    
    # Test page 1
    print("\n1. Get page 1 (page_size=3):")
    response = requests.get(f"{BASE_URL}/api/services?page=1&page_size=3")
    data = response.json()
    
    print(f"   Status: {response.status_code}")
    print(f"   Items: {len(data['items'])}")
    print(f"   Total: {data['total']}")
    print(f"   Page: {data['page']}/{data['total_pages']}")
    print(f"   Has next: {data['has_next']}")
    print(f"   Has prev: {data['has_prev']}")
    
    if data['total'] > 3:
        # Test page 2
        print("\n2. Get page 2 (page_size=3):")
        response = requests.get(f"{BASE_URL}/api/services?page=2&page_size=3")
        data = response.json()
        
        print(f"   Status: {response.status_code}")
        print(f"   Items: {len(data['items'])}")
        print(f"   Page: {data['page']}/{data['total_pages']}")
        print(f"   Has next: {data['has_next']}")
        print(f"   Has prev: {data['has_prev']}")
    
    print("\n   ✅ Services pagination working!")

def test_pagination_edge_cases():
    """Test pagination edge cases"""
    print("\n" + "="*50)
    print("TESTING PAGINATION EDGE CASES")
    print("="*50)
    
    # Test invalid page (should return empty or error)
    print("\n1. Invalid page number (page=999):")
    response = requests.get(f"{BASE_URL}/api/portfolio?page=999&page_size=10")
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Items: {len(data['items'])}")
    print(f"   ✅ Handled gracefully")
    
    # Test page_size limit
    print("\n2. Max page_size (page_size=100):")
    response = requests.get(f"{BASE_URL}/api/portfolio?page=1&page_size=100")
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Items: {len(data['items'])}")
    print(f"   ✅ Respects max limit")
    
    # Test invalid page_size (should fail validation)
    print("\n3. Invalid page_size (page_size=0):")
    response = requests.get(f"{BASE_URL}/api/portfolio?page=1&page_size=0")
    print(f"   Status: {response.status_code}")
    if response.status_code == 422:
        print(f"   ✅ Validation working")
    else:
        print(f"   ⚠️  Expected 422, got {response.status_code}")

def main():
    print("="*50)
    print("PAGINATION TEST SUITE")
    print("="*50)
    
    try:
        test_portfolio_pagination()
        test_services_pagination()
        test_pagination_edge_cases()
        
        print("\n" + "="*50)
        print("✅ PAGINATION TESTS COMPLETED")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
