using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{

    public float speed;
    public float jumpForce = 10;
    private int targetLane = 1;
    private float laneDistance = 3;
    private Rigidbody rb;
    private float distanceToGround;
    public Animator animator;
    private bool isSliding;
    private IEnumerator sliding;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        distanceToGround = GetComponent<Collider>().bounds.extents.y;
    }

    // Update is called once per frame
    void Update()
    {


        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            targetLane++;
            if (targetLane == 3)
                targetLane = 2;
        }

        if (Input.GetKeyDown(KeyCode.LeftArrow)) 
        { 
            targetLane--;
            if (targetLane == -1)
                targetLane = 0;
        }

        if (Input.GetKeyDown(KeyCode.UpArrow) && IsGrounded())
        {
            animator.SetBool("isSliding", false);
            isSliding = false;
            if (sliding != null)
                StopCoroutine(sliding);
            rb.AddForce(Vector3.up * jumpForce, ForceMode.VelocityChange);
        }

        if (Input.GetKeyDown(KeyCode.DownArrow) && IsGrounded() && !isSliding)
        {
            sliding = Slide();
            isSliding = true;
            animator.SetBool("isSliding", true);
            StartCoroutine(sliding);
        }

        Vector3 targetPosition = transform.position.z * Vector3.forward + transform.position.y * Vector3.up;

        if (targetLane == 0) 
        {
            targetPosition += Vector3.left * laneDistance;
        } 
        else if (targetLane == 2) 
        {
            targetPosition += Vector3.right * laneDistance;
        }
        transform.position = targetPosition;
    }

    private void FixedUpdate()
    {
        Vector3 vel = Vector3.forward * speed;
        vel.y = rb.velocity.y;
        rb.velocity = vel;
        rb.AddForce(Vector3.down * 20 * rb.mass);
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.transform.tag == "Obstacle")
        {
            PlayerManager.gameOver = true;
        }
    }

    private bool IsGrounded()
    {
        return Physics.Raycast(transform.position, -Vector3.up, distanceToGround + 0.1f);
    }

    private IEnumerator Slide()
    {
        yield return new WaitForSeconds(1f);

        animator.SetBool("isSliding", false);
        isSliding = false;
    }
}
