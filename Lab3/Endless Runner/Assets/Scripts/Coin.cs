using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Coin : MonoBehaviour
{

    public PlayerManager playerManager;
    public ParticleSystem coinExplosion;

    // Start is called before the first frame update
    void Start()
    {
        playerManager = FindObjectOfType<PlayerManager>();
    }

    // Update is called once per frame
    void Update()
    {
        transform.Rotate(50*Time.deltaTime, 50 * Time.deltaTime, 50 * Time.deltaTime);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Player")
        {
            Instantiate(coinExplosion, transform.position, new Quaternion(-90f, 0f, 0f, 1f));
            Destroy(gameObject);
            playerManager.pickUpCoin();
        }
    }
}
