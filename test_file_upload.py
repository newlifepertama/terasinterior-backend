"""Test file upload"""
import requests
import io
from PIL import Image

BASE_URL = "http://127.0.0.1:8000"

def create_test_image(width=800, height=600, color='red'):
    """Create a test image in memory"""
    img = Image.new('RGB', (width, height), color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_image_upload():
    """Test image upload"""
    print("="*50)
    print("TESTING IMAGE UPLOAD")
    print("="*50)
    
    # Login first
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "admin@terasinterior.com",
        "password": "admin123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Upload valid image
    print("\n1. Upload valid JPEG image:")
    img_bytes = create_test_image()
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{BASE_URL}/api/portfolio/upload-image", 
                            headers=headers, 
                            files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {response.status_code} ✅")
        print(f"   URL: {data['url']}")
        print(f"   Filename: {data['filename']}")
        
        # Verify file is accessible
        file_url = f"{BASE_URL}{data['url']}"
        verify_response = requests.get(file_url)
        if verify_response.status_code == 200:
            print(f"   File accessible: ✅")
        else:
            print(f"   File accessible: ❌ ({verify_response.status_code})")
    else:
        print(f"   Status: {response.status_code} ❌")
        print(f"   Error: {response.text}")
    
    # Test 2: Upload invalid file type
    print("\n2. Upload invalid file type (should fail):")
    files = {'file': ('test.txt', b'This is not an image', 'text/plain')}
    response = requests.post(f"{BASE_URL}/api/portfolio/upload-image",
                            headers=headers,
                            files=files)
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 400 else '❌ FAIL'}")
    
    # Test 3: Upload without auth
    print("\n3. Upload without authentication (should fail):")
    img_bytes = create_test_image()
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{BASE_URL}/api/portfolio/upload-image",
                            files=files)
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 401 else '❌ FAIL'}")

def test_portfolio_with_upload():
    """Test creating portfolio with uploaded image"""
    print("\n" + "="*50)
    print("TESTING PORTFOLIO WITH UPLOADED IMAGE")
    print("="*50)
    
    # Login
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "admin@terasinterior.com",
        "password": "admin123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Upload image
    print("\n1. Upload image:")
    img_bytes = create_test_image(color='blue')
    files = {'file': ('portfolio-test.jpg', img_bytes, 'image/jpeg')}
    upload_response = requests.post(f"{BASE_URL}/api/portfolio/upload-image",
                                   headers=headers,
                                   files=files)
    
    if upload_response.status_code != 200:
        print(f"   Upload failed: {upload_response.status_code}")
        return
    
    image_url = upload_response.json()['url']
    print(f"   Uploaded: {image_url} ✅")
    
    # Create portfolio with uploaded image
    print("\n2. Create portfolio with uploaded image:")
    portfolio_data = {
        "title": "Test Portfolio with Upload",
        "description": "This portfolio uses an uploaded image",
        "category": "Test",
        "image_url": image_url,
        "published": False,
        "order_index": 999
    }
    
    response = requests.post(f"{BASE_URL}/api/portfolio",
                           headers=headers,
                           json=portfolio_data)
    
    if response.status_code == 201:
        data = response.json()
        print(f"   Created portfolio ID: {data['id']} ✅")
        print(f"   Image URL: {data['image_url']}")
        
        # Clean up - delete portfolio
        delete_response = requests.delete(f"{BASE_URL}/api/portfolio/{data['id']}",
                                        headers=headers)
        if delete_response.status_code == 204:
            print(f"   Cleaned up: ✅")
    else:
        print(f"   Failed: {response.status_code}")
        print(f"   Error: {response.text}")

def main():
    print("="*50)
    print("FILE UPLOAD TEST SUITE")
    print("="*50)
    
    try:
        test_image_upload()
        test_portfolio_with_upload()
        
        print("\n" + "="*50)
        print("✅ FILE UPLOAD TESTS COMPLETED")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
