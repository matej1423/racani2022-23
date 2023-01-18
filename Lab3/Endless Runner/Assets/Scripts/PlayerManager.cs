using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerManager : MonoBehaviour
{

    public static bool gameOver;
    public GameObject gameOverPanel;
    public static bool isGameStarted;
    public GameObject startPanel;
    public int coins;
    public Text coinCounter;

    // Start is called before the first frame update
    void Start()
    {
        gameOver = false;
        isGameStarted = false;
        Time.timeScale = 0.0f;
        coins = 0;
    }

    // Update is called once per frame
    void Update()
    {
         if (gameOver)
        {
            Time.timeScale = 0;
            gameOverPanel.SetActive(true);
        }
        if (Input.GetKeyDown(KeyCode.Space))
        {
            isGameStarted = true;
            Time.timeScale = 1.0f;
            startPanel.SetActive(false);
        }
    }

    public void pickUpCoin()
    {
        coins++;
        coinCounter.text = "Coins: " + coins;
    }
}
