"""
https://github.com/langchain-ai/langchain/blob/master/cookbook/forward_looking_retrieval_augmented_generation.ipynb

FLARE will allow the product to always deliver in confidence, with high-quality information.
It basically acts on the idea that when the model starts to get under-confident, it searches the web, and uses that information to continue writing.

This could be a lot more expensive than a single prompt, but it will ensure that we have high quality, backed information.
"""
