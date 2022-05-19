# !bash ./run_main.sh

#python3 './main.py' \
#        --mode 'train' \
#        --lr 2e-4 \
#        --batch_size 10 \
#        --num_epoch 300 \
#        --ny 256 \
#        --nx 256 \
#        --nch 3 \
#        --nker 64 \
#        --wgt 1e2 \
#        --network 'pix2pix' \
#        --data_dir './../../datasets/facaes' \
#        --ckpt_dir './checkpoint' \
#        --log_dir './log' \
#        --result_dir './result'
#

python3 '/opt/ml/fairytale_local/styletransfer_gan/Cycle_GAN/main.py' \
        --mode 'test' \
        --train_continue 'on' \
        --lr 2e-4 \
        --batch_size 4 \
        --num_epoch 200 \
        --ny 256 \
        --nx 256 \
        --nch 3 \
        --nker 64 \
        --wgt_cycle 1e2 \
        --wgt_ident 5e-1 \
        --network 'CycleGAN' \
        --data_dir '/opt/ml/fairytale_local/styletransfer_gan/fairy2photo' \
        --ckpt_dir '/opt/ml/fairytale_local/styletransfer_gan/Cycle_GAN/checkpoint' \
        --log_dir '/opt/ml/fairytale_local/styletransfer_gan/Cycle_GAN/log' \
        --result_dir '/opt/ml/fairytale_local/styletransfer_gan/Cycle_GAN/result'

