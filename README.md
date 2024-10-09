# AMTS Stegnography

This is a project for the paper "Steganography in RGB Images Using Adjacent Mean with Threshold Shifting."

# Example
There is complete example of embedding and extracting information in usage.ipynb.

In the settings section, set C as the carrier,
ED as the information to be embedded,
T as the threshold, and N as the number of bits embedded at each embeddable position.

After settings section, we first encode the embedded information according to the size of N by encode() function. This function will output D and r, these are the encoded information and the remaining bits that cannot form a complete segment.

In the Embed section,
the embed_data() function requires four parameters: the carrier, the encoded information, the number of bits to embed at each embedding point, and the threshold. And the function will output S and EP, where S is the image after embedding the information, and EP is the embedding endpoint.
Next, we execute the embed_endpoint() function to embed EP to S.
Finally, we embed important information such as N, r, and T into the first pixel of the image using the embed_info() function.


