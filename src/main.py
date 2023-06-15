import numpy as np

from screen import Screen

# constants
SCREEN_SIZE = (400, 400)
BACKGROUND = (.3, .4, .6)

ss = SCREEN_SIZE


class Main:

  def __init__(self, spheres):
    self.spheres = spheres
    self.screen = Screen(ss, self.tick)
    self.screen.max_fps = 999
    self.light = norm(np.array((1, 1, 3)))
    self.tick()
    #self.shootRay((0,0,0),(0,0,1))

  def tick(self):
    for i in range(ss[0]):
      for j in range(ss[1]):
        self.screen.setAt(pos=(i, j), color=self.perPixel((i, j), ss))
      self.screen.update()
    self.screen.update()

  def perPixel(self, pos, res):
    pos = np.array(pos)
    res = np.array(res)
    uv = (2 * pos - res) / res[1]
    bounces = 6
    color = np.array((0,0,0), dtype=np.float64)
    point = np.array((0, 0, 0))
    direction = np.array((*uv, -1))
    multiplier = 0.5
    intensity = 1
    for i in range(bounces):
      payload = self.traceRay(point, direction)
      if payload["hit"] == False:
        return color + np.array(BACKGROUND) * 0.7
      color += payload["d"] * payload["sphere"].albedo * intensity

      u = payload["u"]
      n = np.array(payload["normal"])
      direction = reflect(u,n + payload["sphere"].roughness * np.random.uniform(-0.5,0.5,3))
      point = payload["point"]
      intensity *= multiplier
    return color

  def traceRay(self, origin, u):
    origin = np.array(origin)
    u = np.array(u)
    light = self.light
    closest_t = 9999999999
    closest_sphere = None

    for i in self.spheres:
      o = origin - i.pos
      a = np.dot(u, u)
      b = 2 * np.dot(o, u)
      c = np.dot(o, o) - i.r * i.r

      discriminant = b * b - 4 * a * c
      if discriminant < 0:
        continue

      #t0 = (-b + np.sqrt(discriminant)) / (2 * a)
      t = (-b - np.sqrt(discriminant)) / (2 * a)
      if t < closest_t and t > 0.01:
        closest_t = t
        closest_sphere = i

    if closest_sphere == None:
      hit_payload = {"hit": False}
      return hit_payload

    o = origin - closest_sphere.pos
    hit_point = o + u * closest_t
    normal = norm(hit_point)  # - closest_sphere.pos)
    d = max(np.dot(normal, light), 0)

    hit_point += closest_sphere.pos

    hit_payload = {
      "hit": True,
      "point": hit_point,
      "normal": normal,
      "d": d,
      "distance": closest_t,
      "sphere": closest_sphere,
      "u": u
    }

    return hit_payload


def norm(array):
  return array / np.linalg.norm(array)


def reflect(vect, normal):
  return norm(normal - 2 * np.dot(vect, normal) * normal)


class Sphere:

  def __init__(self,
               pos=(0, 0, 0),
               r=0.5,
               albedo=(1, 1, 1),
               roughness=0.2,
               metallic=0):
    self.pos = np.array(pos)
    self.r = r
    self.albedo = np.array(albedo, dtype=np.float64)  # color basicly
    self.roughness = roughness
    self.metallic = metallic

def main():
  spheres = [
    Sphere((0, -201, 0), 200, (0, 1, 1)),
    Sphere((0, 0, -3.5), 1, (1, 0, 1)),

  ] 
  
  Main(spheres)
  
if __name__ == "__main__":
  main()