#include "espnow_manager.h"

// Static variable for broadcast
static uint8_t broadcast_mac[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

ESPNowManager::ESPNowManager() {
    neighbor_count = 0;
    is_initialized = false;
}

bool ESPNowManager::initialize(const char* agent_name, uint8_t capabilities, esp_now_recv_cb_t callback) {
    strncpy(this->agent_name, agent_name, sizeof(this->agent_name) - 1);
    this->agent_name[sizeof(this->agent_name) - 1] = '\0';
    this->agent_capabilities = capabilities;
    
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    // Get MAC address
    uint8_t mac[6];
    WiFi.macAddress(mac);
    memcpy(agent_mac, mac, 6);

    Serial.printf("[ESP-NOW] Agent: %s, MAC: %02X:%02X:%02X:%02X:%02X:%02X, Channel: 1\n", 
                  this->agent_name, agent_mac[0], agent_mac[1], agent_mac[2], agent_mac[3], agent_mac[4], agent_mac[5]);

    if (esp_now_init() != ESP_OK) {
        Serial.println("[ESP-NOW] ERROR: Failed to initialize ESP-NOW");
        return false;
    }
    
    esp_now_register_send_cb(on_data_sent_static);
    esp_now_register_recv_cb(callback);
    
    // Add broadcast peer
    esp_now_peer_info_t peer_info = {};
    memcpy(peer_info.peer_addr, broadcast_mac, 6);
    if (!esp_now_is_peer_exist(broadcast_mac)) {
        if (esp_now_add_peer(&peer_info) != ESP_OK) {
            Serial.println("[ESP-NOW] ERROR: Failed to add broadcast peer");
            return false;
        }
    }
    
    is_initialized = true;
    return true;
}

void ESPNowManager::start() {
    Serial.println("[ESP-NOW] Manager started.");
}

void ESPNowManager::on_data_sent_static(const uint8_t* mac_addr, esp_now_send_status_t status) {
    if (status != ESP_NOW_SEND_SUCCESS) {
        Serial.printf("[ESP-NOW] Send failure to %02X:%02X:%02X:%02X:%02X:%02X\n", mac_addr[0],mac_addr[1],mac_addr[2],mac_addr[3],mac_addr[4],mac_addr[5]);
    }
}

const uint8_t* ESPNowManager::get_agent_mac() {
    return agent_mac;
}

bool ESPNowManager::send_discovery_broadcast() {
    NetworkMessage_t msg;
    msg.type = MSG_DISCOVERY;
    memcpy(msg.sender_mac, agent_mac, 6);
    msg.payload[0] = agent_capabilities;
    msg.payload_length = 1;
    
    return esp_now_send(broadcast_mac, (uint8_t*)&msg, sizeof(NetworkMessage_t)) == ESP_OK;
}

bool ESPNowManager::send_cooperation_request(const uint8_t* target_mac, CooperationAction_t* action) {
    NetworkMessage_t msg;
    msg.type = MSG_COOPERATION_REQUEST;
    memcpy(msg.sender_mac, agent_mac, 6);
    memcpy(msg.payload, action, sizeof(CooperationAction_t));
    msg.payload_length = sizeof(CooperationAction_t);

    return esp_now_send(target_mac, (uint8_t*)&msg, sizeof(NetworkMessage_t)) == ESP_OK;
}

bool ESPNowManager::send_cooperation_response(const uint8_t* target_mac, uint8_t request_id, bool success) {
    NetworkMessage_t msg;
    msg.type = MSG_COOPERATION_RESPONSE;
    memcpy(msg.sender_mac, agent_mac, 6);
    msg.payload[0] = request_id;
    msg.payload[1] = (uint8_t)success;
    msg.payload_length = 2;

    return esp_now_send(target_mac, (uint8_t*)&msg, sizeof(NetworkMessage_t)) == ESP_OK;
}

void ESPNowManager::add_or_update_neighbor(const uint8_t* mac, uint8_t capabilities) {
    for (int i = 0; i < neighbor_count; i++) {
        if (memcmp(neighbors[i].mac, mac, 6) == 0) {
            neighbors[i].last_seen = millis();
            neighbors[i].capabilities = capabilities;
            return;
        }
    }

    if (neighbor_count < MAX_NEIGHBORS) {
        esp_now_peer_info_t peer_info = {};
        memcpy(peer_info.peer_addr, mac, 6);
        peer_info.channel = 1; // Default channel
        
        if (!esp_now_is_peer_exist(mac)) {
            if (esp_now_add_peer(&peer_info) == ESP_OK) {
                memcpy(neighbors[neighbor_count].mac, mac, 6);
                neighbors[neighbor_count].capabilities = capabilities;
                neighbors[neighbor_count].last_seen = millis();
                neighbor_count++;
                Serial.printf("[ESP-NOW] New neighbor added: %02X:%02X:%02X:%02X:%02X:%02X\n", mac[0],mac[1],mac[2],mac[3],mac[4],mac[5]);
            }
        }
    }
}

void ESPNowManager::cleanup_neighbors() {
    unsigned long now = millis();
    for (int i = neighbor_count - 1; i >= 0; i--) {
        if ((now - neighbors[i].last_seen) > NEIGHBOR_TIMEOUT_MS) {
            Serial.printf("[ESP-NOW] Removing inactive neighbor: %02X:%02X:%02X:%02X:%02X:%02X\n", neighbors[i].mac[0],neighbors[i].mac[1],neighbors[i].mac[2],neighbors[i].mac[3],neighbors[i].mac[4],neighbors[i].mac[5]);
            esp_now_del_peer(neighbors[i].mac);
            if (i != neighbor_count - 1) {
                memcpy(&neighbors[i], &neighbors[neighbor_count-1], sizeof(NeighborEntry_t));
            }
            neighbor_count--;
        }
    }
}

bool ESPNowManager::find_neighbor_by_capability(uint8_t capability, NeighborEntry_t* neighbor) {
    if (!neighbor) return false;
    for (int i = 0; i < neighbor_count; i++) {
        if ((neighbors[i].capabilities & capability) != 0) {
            memcpy(neighbor, &neighbors[i], sizeof(NeighborEntry_t));
            return true;
        }
    }
    return false;
}

void ESPNowManager::print_neighbor_table() {
    Serial.printf("--- Neighbor Table (%d) ---\n", neighbor_count);
    for (int i = 0; i < neighbor_count; i++) {
        Serial.printf("Neighbor %d: %02X:%02X:%02X:%02X:%02X:%02X | Caps: 0x%02X\n", 
        i, neighbors[i].mac[0],neighbors[i].mac[1],neighbors[i].mac[2],neighbors[i].mac[3],neighbors[i].mac[4],neighbors[i].mac[5],
        neighbors[i].capabilities);
    }
    Serial.println("-----------------------------");
}