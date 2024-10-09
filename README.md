# AMTS Stegnography

**Home**: [https://github.com/Axisflow/AMTS-Steganography](https://github.com/Axisflow/AMTS-Steganography)

**Authors**: [Zheng-Jie Wang](https://github.com/Axisflow), [Hung-Yu Chen](https://github.com/Ethan01478), Tai-Han Kuo and [Jason Lin](https://github.com/senyalin)

This is a project for the paper "Data Hiding in Color Images Using Adjacent Mean with Threshold Shifting."

## Documentation

There is complete example of embedding and extracting information in `usage.ipynb`.

### Settings

Set `C` as the carrier, `ED` as the information to be embedded, `T` as the threshold, and `N` as the number of bits embedded at each embeddable position.

After settings section, we first encode the embedded information according to the size of `N` by `encode()` function. This function will output `D` and `r`, these are the encoded information and the remaining bits that cannot form a complete segment.

### Embed

The `embed_data()` function requires four parameters: the carrier, the encoded information, the number of bits to embed at each embedding point, and the threshold. This function outputs two results: `S`, the image after embedding the information, and `EP`, the embedding endpoint.

Next, we use the `embed_endpoint()` function to embed `EP` into `S`.

Finally, the `embed_info()` function is used to embed important information such as `N`, `r`, and `T` into the first pixel of the image.
After these steps, we obtain the final image.

### Extract

We first extract `N`, `r` and `T` by `extract_info(S)`.

Next, we extract end point information by `extract_endpoint(S)`.

Finally, the information embedded in the image can be extracted using `extract_data(S, N, T, EP)`.

### Note

If you want to access the quality of the image after embedding the information, you can use the function `PSNR()` in the utility folder within the `image_processor` directory.

## License

AMTS Stegnography is covered with MIT license.
