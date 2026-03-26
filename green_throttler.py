import requests
import urllib3

# Kill insecure cert warnings (standard sysadmin move on local BMC/iLO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Config ---
REDFISH_URL = "https://10.0.0.100/redfish/v1/Chassis/System.Embedded.1/Power"
AUTH = ('root', 'calvin')
MAX_WATTS = 300 
# ---------------------

def get_power_draw():
    try:
        # Timeout tres court pour ne pas bloquer le script si le serveur est down
        res = requests.get(REDFISH_URL, auth=AUTH, verify=False, timeout=3)
        res.raise_for_status()
        
        data = res.json()
        return data.get('PowerControl', [{}])[0].get('PowerConsumedWatts', 0)
    except Exception as e:
        print(f"[ERROR] Redfish API call failed: {e}")
        return None

if __name__ == "__main__":
    current_watts = get_power_draw()
    
    # Mock data pour tester sans avoir de vrai serveur sous la main
    if current_watts is None or current_watts == 0:
        print("[WARN] Using mock data (350W) for testing purposes.")
        current_watts = 350
        
    print(f"[INFO] Current server power draw: {current_watts}W")
    
    if current_watts > MAX_WATTS:
        print(f"[CRITICAL] Power draw ({current_watts}W) exceeds Eco Threshold ({MAX_WATTS}W)!")
        print("[ACTION] Triggering hypervisor power-saving mode... (Dry Run)")
        # Ici on lancerait un playbook Ansible ou une requete vCenter
    else:
        print("[OK] Power consumption is within limits.")