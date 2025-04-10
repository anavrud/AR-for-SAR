using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine;

public class VoiceCommand : MonoBehaviour, IMixedRealitySpeechHandler
{
    [Header("Component References")]
    [SerializeField]
    private InteractiveMapAssembler interactiveMapAssembler;

    [SerializeField]
    private MapToggle mapToggle;

    [SerializeField]
    private MapReset mapReset;

    private void Start()
    {
        // Find references if not assigned
        if (interactiveMapAssembler == null)
            interactiveMapAssembler = FindObjectOfType<InteractiveMapAssembler>();

        if (mapToggle == null)
            mapToggle = FindObjectOfType<MapToggle>();

        if (mapReset == null)
            mapReset = FindObjectOfType<MapReset>();
    }

    // This method is called when a speech command is recognized.
    public void OnSpeechKeywordRecognized(SpeechEventData eventData)
    {
        switch (eventData.Command.Keyword.ToLower())
        {
            case "recenter":
                Debug.Log("Recenter command recognized");
                if (interactiveMapAssembler != null)
                    interactiveMapAssembler.RecenterMapButton();
                else
                    Debug.LogWarning("Map assembler not found for recenter command");
                eventData.Use();
                break;

            case "toggle map":
                Debug.Log("Toggle Map command recognized");
                if (mapToggle != null)
                    mapToggle.ToggleMap();
                else
                    Debug.LogWarning("Map toggle not found for Toggle Map command");
                eventData.Use();
                break;

            case "reset":
                Debug.Log("Reset command recognized");
                if (mapReset != null)
                    mapReset.ResetMap();
                else
                    Debug.LogWarning("Map reset not found for reset command");
                eventData.Use();
                break;
        }
    }

    // Public methods to simulate commands via keyboard
    public void SimulateRecenterCommand()
    {
        Debug.Log("Simulated recenter command");
        if (interactiveMapAssembler != null)
            interactiveMapAssembler.RecenterMapButton();
    }

    public void SimulateToggleCommand()
    {
        Debug.Log("Simulated Toggle Map command");
        if (mapToggle != null)
            mapToggle.ToggleMap();
    }

    public void SimulateResetCommand()
    {
        Debug.Log("Simulated reset command");
        if (mapReset != null)
            mapReset.ResetMap();
    }

    private void OnEnable()
    {
        CoreServices.InputSystem?.RegisterHandler<IMixedRealitySpeechHandler>(this);
    }

    private void OnDisable()
    {
        CoreServices.InputSystem?.UnregisterHandler<IMixedRealitySpeechHandler>(this);
    }
}
