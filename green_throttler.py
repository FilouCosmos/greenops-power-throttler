import requests
import urllib3
import time

# --- Configuration ---
# iDRAC / iLO (Interface de management)
REDFISH_URL = "https://10.0.0.100/redfish/v1/Chassis/System.Embedded.1/Power"
AUTH = ('root', 'calvin')

# Seuil d'alerte écologique (en Watts)
SEUIL_WATTS_ECO = 300 
# ---------------------

# Désactiver les avertissements pour les certificats auto-signés des serveurs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtenir_consommation() -> int:
    """Interroge l'API standard Redfish du serveur physique."""
    try:
        reponse = requests.get(REDFISH_URL, auth=AUTH, verify=False, timeout=5)
        reponse.raise_for_status()
        donnees = reponse.json()
        # Chemin standard Redfish pour récupérer la consommation
        return donnees.get('PowerControl', [{}])[0].get('PowerConsumedWatts', 0)
    except Exception as e:
        print(f"Erreur d'accès Redfish : {e}")
        return 0

def agir_sur_infrastructure(watts: int):
    """Logique de throttling en cas de surconsommation."""
    if watts > SEUIL_WATTS_ECO:
        print(f"!  ALERTE GREENOPS: Serveur à {watts}W (Seuil: {SEUIL_WATTS_ECO}W).")
        print("! Action requise : Migration des VMs non-critiques, ou activation du mode d'économie d'énergie de l'Hyperviseur.")
        # Ici, vous pourriez déclencher un script Ansible ou vCenter
    else:
        print(f"! Empreinte énergétique optimale : {watts}W.")

if __name__ == "__main__":
    print("! Démarrage de la sonde GreenOps via Redfish API...")
    conso_actuelle = obtenir_consommation()
    
    # Pour la démo, si l'API n'est pas dispo, on simule une valeur
    if conso_actuelle == 0:
        print("[Demo Mode] Simulation d'une consommation à 350W")
        conso_actuelle = 350
        
    agir_sur_infrastructure(conso_actuelle)