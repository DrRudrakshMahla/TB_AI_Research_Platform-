from ai.inference import InferenceEngine

class PredictionService:
    def __init__(self,inference_engine:InferenceEngine,quality_engine=None):
        self.inference_engine=inference_engine
        self.quality_engine=quality_engine

    def predict(self,image):
        quality=None
        if self.quality_engine:
            quality=self.quality_engine.evaluate(image)
            if not quality.analysis_allowed:
                return {"status":"blocked","quality":quality}
        result=self.inference_engine.predict(image)
        return {"status":"ok","quality":quality,"result":result}
