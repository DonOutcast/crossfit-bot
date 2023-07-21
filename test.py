class A:

    @classmethod
    def m(cls, name):
        print(name)
        return cls(errors="ee")
        # try:
        #     print(1 / 0)
        # except Exception as e:
        #     return cls(errors=e, ok=False)

print(A().m(name=2))