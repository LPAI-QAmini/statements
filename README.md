# statements

- 数据说明（./data）

  - BoolQ
    - `train/dev.jsonl`: `BoolQ` format data.
    - `train/dev.transformers_format.json`: the transformer format data of original `BoolQ` data.
    - `train/dev.statement.transformers_format.csv`: the statement & transformer format data of original `BoolQ `data.

- question-to-statement

  - `./question-to-statement`
  - 启动脚本：
    - `python q2s.py path_to_input_file path_to_output_file path_to_stanfordCoreNLP`
      - `input_file`: 
        - `BoolQ` format data.
    - 环境依赖：
      - `stanfordcorenlp`

- statement-to-question

  - `./statement-to-question`
  - 启动脚本：
    - `python s2q.py path_to_input_file path_to_output_file`
    - `input_file`:
      - `transformers` format data.
  - 环境依赖：
    - `nltk`

- Classification Script

  - `run_glue.py`

  - 运行命令：

    - ```
      # Finetune on MNLI dataset
      export TASK_NAME=MNLI
      
      python run_glue.py \
        --model_name_or_path bert-large-uncased \
        --task_name $TASK_NAME \
        --do_train \
        --do_eval \
        --max_seq_length 128 \
        --per_device_train_batch_size 32 \
        --learning_rate 2e-5 \
        --num_train_epochs 3.0 \
        --save_steps 10000 \
        --output_dir /tmp/$TASK_NAME/
      ```

    - ```
      # Finetune on BoolQ dataset
      python run_glue.py \
        --model_name_or_path $path_to_model_finetuned_on_MNLI \
        --do_train \
        --do_eval \
        --fp16 \
        --train_file $path_to_train_file \
        --validation_file $path_to_dev_file \
        --max_seq_length 256 \
        --per_device_train_batch_size 12 \
        --per_device_eval_batch_size 12 \
        --learning_rate 2e-5 \
        --num_train_epochs 3.0 \
        --save_steps 10000 \
        --output_dir $path_to_output_path \
        --overwrite_output_dir
      # Note: $path_to_model_finetuned_on_MNLI只加载BERT的编码层参数
      ```

    - ```
      # Prediction on statement data
      python run_glue.py \
        --model_name_or_path  $path_to_model_finetuned_on_BoolQ\
        --do_eval \
        --train_file $none_file \
        --validation_file $path_to_eval_file \
        --overwrite_cache \
        --max_seq_length 256 \
        --per_device_eval_batch_size 32 \
        --learning_rate 2e-5 \
        --num_train_epochs 3.0 \
        --output_dir $path_to_output_path
      ```

  - 环境依赖

    - `datasets`
    - `tranformers`

