/*  Light intensity should ideally be between 2-10, depending on the directional light
 Create a spotlight object and for the character choose Generate Characters
Put this light in the streetlamp
maybe put a sphere with a halo in the streetlamp 
 
 */
using UnityEngine;
using System.Collections.Generic;
using System.Collections;
public class GenerateLight : MonoBehaviour
{
    List<Color> LightColors = new List<Color>() {
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0, 0, 0, 1),
        new Color(0.04f, 1, 0.04f, 1),
        new Color(0.04f, 1, 0.04f, 1)
};

    Light lt;

    void Start()
    {
        lt = GetComponent<Light>();
    }

    private IEnumerator Coroutine()
    {
        int index = Random.Range(0, LightColors.Count - 1);
        yield return new WaitForSeconds(0.42f);
        // set light color
        lt.color = LightColors[index];


    }
    public GameObject character;
    void Update()
    {
        StartCoroutine(Coroutine());
        transform.LookAt(character.transform);
    }
}