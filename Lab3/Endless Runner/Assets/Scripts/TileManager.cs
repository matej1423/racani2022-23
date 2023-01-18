using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileManager : MonoBehaviour
{

    public GameObject[] tilePrefabs;
    public GameObject emptyTile;
    public float zSpawn = 0;
    private float tileLength = 10;
    public int numberOfActiveTiles = 8;
    public Transform playerTransform;
    private List<GameObject> activeTiles = new List<GameObject>();
    private List<GameObject> activeCoins = new List<GameObject>();
    public GameObject coin; 

    // Start is called before the first frame update
    void Start()
    {
        for (int i = 0; i < numberOfActiveTiles; i++)
        {
            if (Random.Range(0, 4) == 0 || i == 0)
                SpawnTile(-1);
            else
                SpawnTile(Random.Range(0, tilePrefabs.Length));
        }

    }

    // Update is called once per frame
    void Update()
    {
        if (playerTransform.position.z - 20 > zSpawn - numberOfActiveTiles*tileLength)
        {
            if (Random.Range(0, 4) == 0)
                SpawnTile(-1);
            else
                SpawnTile(Random.Range(0, tilePrefabs.Length));
            Destroy(activeTiles[0]);
            activeTiles.RemoveAt(0);
            Destroy(activeCoins[0]);
            activeCoins.RemoveAt(0);
        }

    }

    public void SpawnTile(int index)
    {
        GameObject tile;
        if (index == -1)
            tile = Instantiate(emptyTile, Vector3.forward * zSpawn, transform.rotation);
        else
            tile = Instantiate(tilePrefabs[index], Vector3.forward * zSpawn, transform.rotation);
        float[] choices = new float[] { -3f, 3f, 0f };
        GameObject activeCoin = Instantiate(coin, Vector3.forward * zSpawn + new Vector3(choices[Random.Range(0, choices.Length)], 1f, -5f), coin.transform.rotation);
        activeTiles.Add(tile);
        activeCoins.Add(activeCoin);
        zSpawn += tileLength;
    }
}
