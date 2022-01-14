

## ���������� ���� � �������� ���������� ������������ ���������
addpath(genpath('./m'))

## ��������� �������� ������
load data/steam.mat
steam

## ���������� ������ ���������� ������������ ��������� 
##     y = X * beta = beta1 + beta2 * x 
## � ������������ beta2 >= 0

x = [2; 4; 10; 12];        # ���������� ������������ �������
y = [2; 8.5; 18; 25];        # ����� �������������� ����
epsilon = [2; 1.5; 2.5; 1.5];  # ������� ������� ������ ��� y_i

X = [ x.^0 x ];                               # ������� �������� ���������� ��� beta1 � beta2
lb = [-inf 0];                                # ������ ������� beta1 � beta2
irp_steam = ir_problem(X, y, epsilon, lb);



## ������ ������������ ���������
##figure
##ir_scatter(irp_steam);   
##xlim([0 22])
##ylim([-10 260])
##set(gca, 'fontsize', 12)
##title('Steam generator performance');
##xlabel('Fuel consumption');
##ylabel('Steam quantity');



## ����������� ������������� ��������������� ���������
figure
ir_plotbeta(irp_steam)
grid on
set(gca, 'fontsize', 12)
xlabel('\beta_1')
ylabel('\beta_2')

## ������� ������������ ������ ���������� ������ y = beta1 + beta2 * x 
b_int = ir_outer(irp_steam)



## ������� ��������������� ��������� ������ ���������� ������������ ���������
vertices = ir_beta2poly(irp_steam)

## ������� � �������� ��������� ������� ��������������� ��������� 
[rhoB, b1, b2] = ir_betadiam(irp_steam)



## ������� ������������ ������ ���������� ������ y = beta1 + beta2 * x 
b_int = ir_outer(irp_steam)

## �������� ������ ���������� 
b_maxdiag = (b1 + b2) / 2    # ��� �������� ���������� ��������� ��������������� ���������

b_gravity = mean(vertices)   # ��� ����� ������� ��������������� ��������� 

b_lsm = (X \ y)'             # ������� ���������� ���������

## �������� ������
plot(b_maxdiag(1), b_maxdiag(2), ';����� ����. ���������;mo')
plot(b_gravity(1), b_gravity(2), ';����� �������;ks')
plot(b_lsm(1), b_lsm(2), ';���;rx')
legend()

figure 
xlimits = [-5 15];
ir_plotmodelset(irp_steam, xlimits)     # ������� ���������� ������������
hold on
ir_scatter(irp_steam,'b.')              # ������������ ���������
#ir_plotline(b_maxdiag, xlimits, 'r-')   # ����������� � �����������, ���������� ��� ����� ���������� ��������� ��
#ir_plotline(b_gravity, xlim, 'b--')     # ����������� � �����������, ���������� ��� ����� ������� ��  
#ir_plotline(b_lsm, xlim, 'b--')         # ����������� � �����������, ���������� ���
#ir_scatter(ir_problem(Xp,ypmid,yprad),'ro')

grid on
set(gca, 'fontsize', 12)
xlabel('x')
ylabel('y')

figure 
x_p = [2; 10; -1; 5; 13];
ir_plotmodelset(irp_steam, xlimits)
hold on
ir_scatter(irp_steam,'b.')
hold on 
X_p = [x_p.^0 x_p];
y_p = ir_predict(irp_steam, X_p);
ypmid = mean(y_p,2);
yprad = 0.5 * (y_p(:,2) - y_p(:,1));
ir_scatter(ir_problem(X_p,ypmid,yprad),'k.');
grid on
