using System;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GPSDisplayUI : MonoBehaviour
{
    [SerializeField] private GPSSocketClient gpsManager;

    [Header("UI References")]
    [SerializeField] private TextMeshProUGUI coordinatesText;
    [SerializeField] private TextMeshProUGUI statusText;
    [SerializeField] private TextMeshProUGUI timestampText;

    private void Start()
    {
        // Find the manager if not assigned
        if (gpsManager == null)
            gpsManager = FindObjectOfType<GPSSocketClient>();

        // Set up the UI
        if (gpsManager != null)
        {
            gpsManager.OnGPSDataUpdated += OnGPSDataUpdated;
        }
        else
        {
            Debug.LogError("GPSDataManager not found!");
        }

        // Set initial UI state
        UpdateUI();
    }

    private void OnDestroy()
    {
        if (gpsManager != null)
            gpsManager.OnGPSDataUpdated -= OnGPSDataUpdated;
    }

    // Remove the Update method - we don't need to update every frame
    // We'll update only when new GPS data arrives

    private void OnGPSDataUpdated(GPSData data)
    {
        // This will be called only when new GPS data is received
        UpdateUI();
    }

    private void UpdateUI()
    {
        if (gpsManager == null)
            return;

        if (statusText != null)
        {
            // Include connection status in the status text instead of using an indicator
            string statusPrefix = gpsManager.IsConnected ? "Connected" : "Disconnected";
            string dataStatus = gpsManager.IsConnected ?
                (gpsManager.CurrentGPSData.valid ? " - Valid GPS data" : " - No valid GPS data") :
                "";

            statusText.text = $"{statusPrefix}{dataStatus}: {gpsManager.StatusMessage}";
        }

        if (coordinatesText != null)
        {
            if (gpsManager.IsConnected && gpsManager.CurrentGPSData.valid)
            {
                coordinatesText.text = $"Latitude: {gpsManager.CurrentGPSData.latitude:F6}\n" +
                                      $"Longitude: {gpsManager.CurrentGPSData.longitude:F6}\n" +
                                      $"Altitude: {gpsManager.CurrentGPSData.altitude:F2} m";
            }
            else
            {
                coordinatesText.text = "No valid GPS data available";
            }
        }

        if (timestampText != null)
        {
            if (gpsManager.IsConnected)
            {
                TimeSpan timeSinceUpdate = DateTime.Now - gpsManager.LastUpdateTime;
                timestampText.text = $"Last update: {timeSinceUpdate.TotalSeconds:F1} seconds ago";
            }
            else
            {
                timestampText.text = "Not connected";
            }
        }
    }
}
