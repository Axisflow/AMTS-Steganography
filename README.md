# AMTS Stegnography

This is a project for the paper "Steganography in RGB Images Using Adjacent Mean with Threshold Shifting."

# Example
There is complete example of embedding and extracting information in usage.ipynb.

In the settings section, set C as the carrier,
ED as the information to be embedded,
T as the threshold, and N as the number of bits embedded at each embeddable position.

After settings section, we first encode the embedded information according to the size of N by encode() function. This function will output D and r, these are the encoded information and the remaining bits that cannot form a complete segment.

In the Embed section,
the embed_data() function requires four parameters: the carrier, the encoded information, the number of bits to embed at each embedding point, and the threshold. This function outputs two results: S, the image after embedding the information, and EP, the embedding endpoint.
Next, we use the embed_endpoint() function to embed EP into S.
Finally, the embed_info() function is used to embed important information such as N, r, and T into the first pixel of the image.
After these steps, we obtain the final image.

In the Extract section,
we first extract N, r and T by extract_info(S).
Next, we extract end point information by extract_endpoint(S).
Finally, the information embedded in the image can be extracted using extract_data(S, N, T, EP).

NOTE:
If you want to assess the quality of the image after embedding the information, you can use the PSNR function in the utility folder within the image_processor directory.


