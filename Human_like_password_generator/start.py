from Human_like_password_generator.generate_password import generate_password






def start():
    gen_pswd = generate_password()
    print(gen_pswd.__next__())
    print(gen_pswd.__next__())
    print(gen_pswd.__next__())