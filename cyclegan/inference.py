## 라이브러리 추가하기
import argparse

from train import *

def main(args):
    ## 트레이닝 파라메터 설정하기
    lr = args.lr

    batch_size = args.batch_size

    data_dir = args.data_dir
    ckpt_dir = args.ckpt_dir

    ny = args.ny
    nx = args.nx
    nch = args.nch
    nker = args.nker

    norm = args.norm

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print("batch size: %d" % batch_size)

    print("data dir: %s" % data_dir)
    print("ckpt dir: %s" % ckpt_dir)
    # print("log dir: %s" % log_dir)

    print("device: %s" % device)

    ## 디렉토리 생성하기
    result_dir_test = os.path.join(data_dir, 'result')

    if not os.path.exists(result_dir_test):
        os.makedirs(os.path.join(result_dir_test))

    ## 네트워크 학습하기
    transform_test = transforms.Compose([Resize(shape=(ny, nx, nch)), Normalization(mean=MEAN, std=STD)])

    # dataset_test_a = Dataset(data_dir=os.path.join(data_dir, 'result'), transform=transform_test, data_type='a')
    # loader_test_a = DataLoader(dataset_test_a, batch_size=batch_size, shuffle=False, num_workers=NUM_WORKER)

    # 그밖에 부수적인 variables 설정하기
    # num_data_test_a = len(dataset_test_a)
    # num_batch_test_a = np.ceil(num_data_test_a / batch_size)

    dataset_test_b = Inference_Dataset(data_dir=os.path.join(data_dir, 'image'), transform=transform_test)
    loader_test_b = DataLoader(dataset_test_b, batch_size=batch_size, shuffle=False, num_workers=NUM_WORKER)

    print("loader_test_b len : ", len(loader_test_b))
    # 그밖에 부수적인 variables 설정하기
    num_data_test_b = len(dataset_test_b)
    num_batch_test_b = np.ceil(num_data_test_b / batch_size)
    
    netG_a2b = CycleGAN(in_channels=nch, out_channels=nch, nker=nker, norm=norm, nblk=9).to(device)
    netG_b2a = CycleGAN(in_channels=nch, out_channels=nch, nker=nker, norm=norm, nblk=9).to(device)

    netD_a = Discriminator(in_channels=nch, out_channels=1, nker=nker, norm=norm).to(device)
    netD_b = Discriminator(in_channels=nch, out_channels=1, nker=nker, norm=norm).to(device)

    init_weights(netG_a2b, init_type='normal', init_gain=0.02)
    init_weights(netG_b2a, init_type='normal', init_gain=0.02)

    init_weights(netD_a, init_type='normal', init_gain=0.02)
    init_weights(netD_b, init_type='normal', init_gain=0.02)

    ## Optimizer 설정하기
    optimG = torch.optim.Adam(itertools.chain(netG_a2b.parameters(), netG_b2a.parameters()), lr=lr, betas=(0.5, 0.999))
    optimD = torch.optim.Adam(itertools.chain(netD_a.parameters(), netD_b.parameters()), lr=lr, betas=(0.5, 0.999))

    ## 그밖에 부수적인 functions 설정하기
    fn_tonumpy = lambda x: x.to('cpu').detach().numpy().transpose(0, 2, 3, 1)
    fn_denorm = lambda x: (x * STD) + MEAN


    # TEST MODE
    netG_a2b, netG_b2a, \
    netD_a, netD_b, \
    optimG, optimD, _ = load(ckpt_dir=ckpt_dir,
                                    netG_a2b=netG_a2b, netG_b2a=netG_b2a,
                                    netD_a=netD_a, netD_b=netD_b,
                                    optimG=optimG, optimD=optimD)
    
    with torch.no_grad():
        netG_a2b.eval()
        netG_b2a.eval()

        # 'b' domain to 'a' domain
        for batch, data in enumerate(loader_test_b, 1):
            # forward pass
            input_ = data['input'].to(device)

            output_ = netG_b2a(input_)

            # Tensorboard 저장하기
            input_ = fn_tonumpy(fn_denorm(input_))
            output_ = fn_tonumpy(fn_denorm(output_))

            for j in range(input_.shape[0]):
                id = batch_size * (batch - 1) + j

                input_sample = input_[j]
                output_sample = output_[j]

                input_sample = np.clip(input_sample, a_min=0, a_max=1)
                output_sample = np.clip(output_sample, a_min=0, a_max=1)

                plt.imsave(os.path.join(result_dir_test, '%04d_input_b.png' % id), input_sample)
                plt.imsave(os.path.join(result_dir_test, '%04d_output_a.png' % id), output_sample)

                print("TEST : BATCH %04d / %04d | " % (id + 1, num_data_test_b))
                    
    

if __name__ == "__main__":
    ## Parser 생성하기
    parser = argparse.ArgumentParser(description="CycleGAN Inference",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--lr", default=2e-4, type=float, dest="lr")
    parser.add_argument("--batch_size", default=4, type=int, dest="batch_size")

    parser.add_argument("--data_dir", default="./datasets", type=str, dest="data_dir")
    parser.add_argument("--ckpt_dir", default="./checkpoint", type=str, dest="ckpt_dir")
    parser.add_argument("--log_dir", default="./log", type=str, dest="log_dir")

    parser.add_argument("--ny", default=256, type=int, dest="ny")
    parser.add_argument("--nx", default=256, type=int, dest="nx")
    parser.add_argument("--nch", default=3, type=int, dest="nch")
    parser.add_argument("--nker", default=64, type=int, dest="nker")
    parser.add_argument("--norm", default='inorm', type=str, dest="norm")

    args = parser.parse_args()

    main(args)
