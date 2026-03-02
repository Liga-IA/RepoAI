#ifndef ESPNOW_MANAGER_H_
#define ESPNOW_MANAGER_H_

#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

// Configurações da rede
#define MAX_NEIGHBORS 10
#define DISCOVERY_INTERVAL_MS 5000
#define NEIGHBOR_TIMEOUT_MS 15000

// Tipos de mensagem e capacidade
enum MessageType { MSG_DISCOVERY = 1, MSG_COOPERATION_REQUEST = 4, MSG_COOPERATION_RESPONSE = 5 };
enum CapabilityType { 
    CAP_SENSOR_LIGHT = 0x01, 
    CAP_SENSOR_ULTRASONIC = 0x02, 
    CAP_ACTUATOR_BUZZER = 0x04, 
    CAP_ACTUATOR_LED = 0x08,
    CAP_SENSOR_TEMP_HUMID = 0x10, // DHT11
    CAP_SENSOR_TEMP_ANALOG = 0x20, // LM35
    CAP_SENSOR_IR = 0x40, // IR Receiver
    CAP_SENSOR_POT = 0x80 // Potentiometer
};

// Estruturas
typedef struct { uint8_t mac[6]; uint32_t last_seen; uint8_t capabilities; } NeighborEntry_t;
typedef struct { uint8_t type; uint8_t sender_mac[6]; uint8_t payload[16]; uint8_t payload_length; } NetworkMessage_t;
typedef struct { uint8_t action_type; uint8_t param_length; uint8_t priority; uint8_t parameters[10]; } CooperationAction_t;

// Tipo da função de callback para recebimento de dados
typedef void (*esp_now_recv_cb_t)(const uint8_t *mac_addr, const uint8_t *data, int len);

class ESPNowManager {
private:
    NeighborEntry_t neighbors[MAX_NEIGHBORS];
    uint8_t neighbor_count;
    
    uint8_t agent_mac[6];
    uint8_t agent_capabilities;
    char agent_name[16];
    bool is_initialized;

    static void on_data_sent_static(const uint8_t* mac_addr, esp_now_send_status_t status);
    
public:
    ESPNowManager();
    
    bool initialize(const char* agent_name, uint8_t capabilities, esp_now_recv_cb_t callback);
    void start(); // Agora vazia, mas mantida por consistência
    
    const uint8_t* get_agent_mac();
    void add_or_update_neighbor(const uint8_t* mac, uint8_t capabilities);
    void cleanup_neighbors();

    bool send_discovery_broadcast();
    bool send_cooperation_request(const uint8_t* target_mac, CooperationAction_t* action);
    bool send_cooperation_response(const uint8_t* target_mac, uint8_t request_id, bool success);
    
    bool find_neighbor_by_capability(uint8_t capability, NeighborEntry_t* neighbor);
    void print_neighbor_table();
};

#endif