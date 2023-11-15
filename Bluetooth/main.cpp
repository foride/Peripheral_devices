#include <cstdio>
#include <Winsock2.h>
#include <Ws2bth.h>
#include <BluetoothAPIs.h>

#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Bthprops.lib")

// struktura z parametrami wyszukiwania urzadzen BT
BLUETOOTH_DEVICE_SEARCH_PARAMS bt_dev_search_params = {
        sizeof(BLUETOOTH_DEVICE_SEARCH_PARAMS),
        1,
        0,
        1,
        1,
        1,
        20,
        nullptr
};

const int MAX_BT_RADIOS = 10;
const int MAX_BT_DEV = 10;
int bt_radio_id = 0;
int bt_dev_id = 0;

// struktura z parametrami wyszukiwania adaptera BT
BLUETOOTH_FIND_RADIO_PARAMS bt_find_radio_params = { sizeof(BLUETOOTH_FIND_RADIO_PARAMS) };
// struktura z parametrami adaptera BT
BLUETOOTH_RADIO_INFO bt_radio_info = { sizeof(BLUETOOTH_RADIO_INFO), 0, };
// znalezione adaptery BT
HANDLE radios[MAX_BT_RADIOS];
// znaleziony adapter BT
HBLUETOOTH_RADIO_FIND bt_radio_find;
BLUETOOTH_DEVICE_INFO devices[MAX_BT_DEV];
HBLUETOOTH_DEVICE_FIND bt_dev_find;

int main()
{
    // wyszukiwanie pierwszego adaptera BT
    bt_radio_find = BluetoothFindFirstRadio(&bt_find_radio_params, &radios[bt_radio_id]);
    bt_radio_id++;
    if (bt_radio_find == nullptr) {
        printf("Nie znaleziono zadnego adaptera Bluetooth! Kod bledu: %lu\n", GetLastError());
    }   // wyszukiwanie kolejnych adapterów BT
    else {
        while (BluetoothFindNextRadio(bt_radio_find, &radios[bt_radio_id])) {
            bt_radio_id++;
            if (bt_radio_id == MAX_BT_RADIOS - 1) {
                bt_radio_id--;
                printf("Znaleziono wiecej niz 10 adapterow Bluetooth!\n");
                break;
            }
        }
    }

    for (int i = 0; i < bt_radio_id; i++) {
        // pobieranie informacji o danym adapterze i umieszczanie ich w strukturze przechowujacej te dane
        Sleep(500);
        BluetoothGetRadioInfo(radios[i], &bt_radio_info);
        wprintf(L"\nUrzadzenie: %d", i);
        wprintf(L"\n\tNazwa: %s", bt_radio_info.szName);
        wprintf(L"\n\tAdres MAC: %02X:%02X:%02X:%02X:%02X:%02X", bt_radio_info.address.rgBytes[5],
                bt_radio_info.address.rgBytes[4], bt_radio_info.address.rgBytes[3], bt_radio_info.address.rgBytes[2],
                bt_radio_info.address.rgBytes[1], bt_radio_info.address.rgBytes[0]);
        wprintf(L"\n\tKlasa: 0x%08x", bt_radio_info.ulClassofDevice);
        wprintf(L"\n\tProducent: 0x%04x\n", bt_radio_info.manufacturer);
    }

    if (!BluetoothFindRadioClose(bt_radio_find)) printf("Blad zamykania wyszukiwania adapterow BT.");

    int choose_radio = 0;
    printf("\nWybierz adapter:\n>");
    scanf_s("%d", &choose_radio);
    printf("\nWybrano adapter %d.\n", choose_radio);

    printf("\nWyszukiwanie urzadzen bluetooth\n");
    // ustawianie adaptera dla danych parametrow wyszukiwania urzadzen BT
    bt_dev_search_params.hRadio = radios[choose_radio];

    devices[0].dwSize = sizeof(BLUETOOTH_DEVICE_INFO);
    bt_dev_find = BluetoothFindFirstDevice(&bt_dev_search_params, &devices[0]);

    if (bt_dev_find == nullptr) {
        printf("\nNie znaleziono zadnych urzadzen Bluetooth!");
        BluetoothFindDeviceClose(bt_dev_find);
        return 0;
    }
    else {
        bt_dev_id++;
        devices[bt_dev_id].dwSize = sizeof(BLUETOOTH_DEVICE_INFO);
        while (BluetoothFindNextDevice(bt_dev_find, &devices[bt_dev_id])) {
            bt_dev_id++;
            devices[bt_dev_id].dwSize = sizeof(BLUETOOTH_DEVICE_INFO);
        }
        if (BluetoothFindDeviceClose(bt_dev_find)) printf("\nKoniec wyszukiwania urzadzen.");
        else printf("\nBlad konca wyszukiwania urzadzen.");
    }

    printf("\nZnaleziono %d urzadzen.", bt_dev_id);

    for (int i = 0; i < bt_dev_id; i++) {
        Sleep(500);
        wprintf(L"\nUrzadzenie: %d", i);
        wprintf(L"\n\tNazwa: %s", devices[i].szName);
        wprintf(L"\n\tAdres MAC: %02X:%02X:%02X:%02X:%02X:%02X", devices[i].Address.rgBytes[5],
                devices[i].Address.rgBytes[4], devices[i].Address.rgBytes[3], devices[i].Address.rgBytes[2],
                devices[i].Address.rgBytes[1], devices[i].Address.rgBytes[0]);
        wprintf(L"\n\tKlasa: 0x%08x", devices[i].ulClassofDevice);
        wprintf(L"\n\tPolaczone: %s\r\n", devices[i].fConnected ? L"true" : L"false");
        wprintf(L"\tUwierzytelnione: %s\r\n", devices[i].fAuthenticated ? L"true" : L"false");
        wprintf(L"\tZapamietane: %s\r\n", devices[i].fRemembered ? L"true" : L"false");
    }

    int choose_dev = 0;
    printf("\nWybierz urzadzenie:\n>");
    scanf_s("%d", &choose_dev);
    printf("\nWybrano urzadzenie numer %d.\n", choose_dev);

    // autentykacja polaczenia miedzy wybranym adapterem z wybranym urzadzeniem BT
    if (radios[choose_radio] != nullptr && !devices[choose_dev].fAuthenticated)
        BluetoothAuthenticateDeviceEx(nullptr, radios[choose_radio], &devices[choose_dev], nullptr, MITMProtectionRequired);

    // czesc odpowiedzialna za otwarcie gniazda i nawiazanie polaczenia
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Nieudana proba inicjalizacji WinSock");
        return 1;
    }
    // ustawianie gniazda
    SOCKET btSocket = socket(AF_BTH, SOCK_STREAM, BTHPROTO_RFCOMM);
    if (btSocket == INVALID_SOCKET) {
        printf("Nie udalo sie utworzyc socketa bluetooth: %d", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    SOCKADDR_BTH serverAddr;
    serverAddr.addressFamily = AF_BTH;
    serverAddr.serviceClassId = OBEXObjectPushServiceClass_UUID;
    // OBEXObjectPushServiceClass_UUID;
    serverAddr.port = BT_PORT_ANY;
    serverAddr.btAddr = devices[choose_dev].Address.ullLong;

    if (connect(btSocket, (SOCKADDR*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        printf("Nie udalo sie polaczyc!\n Error numer: %d", WSAGetLastError());
        closesocket(btSocket);
        WSACleanup();
        return 1;
    }
    printf("Polaczenie udane!\n");


    closesocket(btSocket);
    WSACleanup();


    return 0;
}