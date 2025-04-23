# Attribution

This project incorporates data from [Amazon Berkeley Objects (ABO) Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html), which is licensed under
[Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/)

Credit for the data, including all images and 3D models:
```
Amazon.com
```
Credit for building the ABO dataset, archives and benchmark sets:
```
Matthieu Guillaumin (Amazon.com), Thomas Dideriksen (Amazon.com), Kenan Deng (Amazon.com), Himanshu Arora (Amazon.com), Arnab Dhua (Amazon.com), Xi (Brian) Zhang (Amazon.com), Tomas Yago-Vicente (Amazon.com), Jasmine Collins (UC Berkeley), Shubham Goel (UC Berkeley), Jitendra Malik (UC Berkeley)
```

## Publication
Based on the paper: [ABO: Dataset and Benchmarks for Real-World 3D Object Understanding](https://amazon-berkeley-objects.s3.amazonaws.com/static_html/ABO_CVPR2022.pdf) ([arxiv.org](https://arxiv.org/abs/2110.06199))
```
@article{collins2022abo,
  title={ABO: Dataset and Benchmarks for Real-World 3D Object Understanding},
  author={Collins, Jasmine and Goel, Shubham and Deng, Kenan and Luthra, Achleshwar and
          Xu, Leon and Gundogdu, Erhan and Zhang, Xi and Yago Vicente, Tomas F and
          Dideriksen, Thomas and Arora, Himanshu and Guillaumin, Matthieu and
          Malik, Jitendra},
  journal={CVPR},
  year={2022}
}
```

## Data Usage and Modifications
Data used:
* [abo-listings.tar](https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-listings.tar)

Modifications:
* Merged all listings JSON files into a single file: `listings_3d.json.gz`
* Excluded listings without the key `'3dmodel_id'`
* Merged multiple listings sharing the same `'item_id'`, due to regional listings:
   * Conflicts are resolved by taking the value from the `'country'=='US'` listing
