# 12. ONNX -> ATC -> OM -> AscendCL

这一章记录昇腾静态推理部署的常见链路。没有昇腾机器时，也可以先理解每一步在做什么。

## 1. 链路总览

```text
PyTorch model
  -> export ONNX
  -> ATC convert
  -> model.om
  -> AscendCL application
  -> Ascend NPU
```

每一步都可能失败。不要把模型转换当成简单文件格式转换。

## 2. PyTorch 导出 ONNX

示意代码：

```python
import torch

model.eval()
dummy = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=17,
    dynamic_axes={
        "input": {0: "batch"},
        "output": {0: "batch"},
    },
)
```

LLM 导出会更复杂。大模型通常不一定走 ONNX 静态部署路线，尤其是动态 generation、KV cache、custom op 较多时。这里先理解 CV/普通模型的静态推理链路。

## 3. ATC 转 OM

ATC 命令的具体参数会随 CANN 版本和芯片型号变化。常见结构类似：

```bash
atc \
  --model=model.onnx \
  --framework=5 \
  --output=model \
  --input_format=NCHW \
  --input_shape="input:1,3,224,224" \
  --soc_version=Ascend310P3
```

含义：

- `--model`：输入模型。
- `--framework`：源框架类型，ONNX 常见是 `5`，以你安装版本文档为准。
- `--output`：输出名前缀，通常生成 `model.om`。
- `--input_shape`：输入 shape。
- `--soc_version`：目标昇腾芯片型号。

要点：

- `soc_version` 必须和硬件匹配。
- dynamic shape 需要看 ATC 支持方式。
- 不支持的 op 会在转换阶段暴露。
- 转换成功不代表精度一定一致，还要做输出对齐。

## 4. AscendCL 加载 OM

推理程序要做的事情：

```text
aclInit
aclrtSetDevice
aclmdlLoadFromFile
prepare input dataset
aclmdlExecute
read output dataset
aclmdlUnload
aclFinalize
```

可以把 AscendCL 看成“部署程序直接操作昇腾 runtime 的 C/C++ API”。

## 5. 常见失败点

### ONNX 导出失败

原因可能是：

- PyTorch op 不支持导出。
- control flow 太动态。
- 自定义 op 没有 symbolic。
- opset 版本不合适。

### ATC 转换失败

原因可能是：

- CANN 不支持某个 ONNX op。
- 输入 shape 没写对。
- dtype 不支持。
- dynamic shape 配置不对。
- `soc_version` 错了。

### 运行时输出不一致

原因可能是：

- 预处理不一致。
- layout 不一致。
- 精度转换影响。
- 后处理不一致。
- 模型导出时训练/推理模式不一致。

## 6. 建议记录模板

```text
model:
source framework:
opset:
CANN version:
soc_version:
ATC command:
input_shape:
conversion result:
runtime result:
accuracy comparison:
error log:
fix:
```

## 参考

- PyTorch ONNX Export: https://docs.pytorch.org/docs/stable/onnx.html
- ONNX Concepts: https://onnx.ai/onnx/intro/concepts.html
- Huawei Ascend documentation: https://www.hiascend.com/document
- Huawei CANN: https://www.hiascend.com/en/cann

