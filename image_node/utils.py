import numpy as np

class Coordinate_Transformation():
        '''
        座標変換
        input:
                画像座標系におけるトマトの位置: u, v(pixel)
                カメラからみたトマトの奥行: Z(cm)
                カメラの内部パラメータ  焦点距離: fx, fy、中心座標: cx, cy
        output:
                アーム座標におけるトマトの座標 X, Y, Z(cm)
        '''
        cam_pos=np.array([100, 100, 100])
        arm_pos=np.array([200, 200, 70])
        world_pos=np.array([0, 0, 0])
        cam_rotation_matrix=np.array([[1,0,0],[0,1,0], [0,0,1]])
        cam_translation_vector=world_pos-cam_pos
        arm_rotation_matrix=np.array([[1,0,0],[0,1,0], [0,0,1]])
        arm_translation_vector=arm_pos-world_pos

        def __init__(self,R):
                self.fx = R[0]
                self.fy = R[1]
                self.cx = R[2]
                self.cy = R[3]

        def transformation(self,u,v,Z):
                #img→cam
                camera_coordinates=self.image_to_camera(u,v,Z)
                #image→arm
                world_coordinates=self.camera_to_world(camera_coordinates,self.cam_rotation_matrix,self.cam_translation_vector)
                #target coordinates
                target_coordinates=self.world_to_arm(world_coordinates,self.arm_rotation_matrix,self.arm_translation_vector)
                return target_coordinates
        
        def tf(self,result_pos):
                target_pos= np.empty((0, 3))
                for camera_coordinates in result_pos :              
                    #image→arm
                    world_coordinates=self.camera_to_world(camera_coordinates,self.cam_rotation_matrix,self.cam_translation_vector)
                    #target coordinates
                    target_coordinates=self.world_to_arm(world_coordinates,self.arm_rotation_matrix,self.arm_translation_vector)
                    target_pos= np.vstack((target_pos, target_coordinates))
                    print(target_pos)
                return target_pos
        
        def image_to_camera(self,u, v, Z):
                X_c = (u - self.cx) * Z / self.fx 
                Y_c = (v - self.cy) * Z / self.fy
                Z_c = Z
                camera_coordinates = np.array([X_c, Y_c, Z_c])
                return camera_coordinates
        
        def camera_to_world(self,camera_coordinates,rotation_matrix,translation_vector):
                world_coordinates = rotation_matrix @ camera_coordinates + translation_vector
                return world_coordinates  

        def world_to_arm(self,camera_coordinates,rotation_matrix,translation_vector):
                target_coordinates = rotation_matrix @ camera_coordinates + translation_vector
                return target_coordinates
                
class Maturity_Judgment():
        '''
        '''
        def __init__(self):
                pass

        def judgment(self):
               pass
        
def main():
   #debag
   #R=[100,200,10,10]
   #node=Coordinate_Transformation(R)
   #target_coordinates=node.transformation(30,40,100)
   #print(target_coordinates)
   pass

if __name__ == '__main__':
    main()
