from django.shortcuts import render, redirect
import random

def index(request):
    # Initialize game state in session if not already set
    if 'number' not in request.session:
        request.session['number'] = random.randint(1, 100)
        request.session['attempts'] = 0
        request.session['game_over'] = False

    message = ''
    guess = None
    game_over = request.session.get('game_over', False)

    if request.method == 'POST' and not game_over:
        try:
            guess = int(request.POST.get('guess'))
            request.session['attempts'] += 1
            number = request.session['number']

            if guess < number:
                message = 'Your guess is low 👇'
            elif guess > number:
                message = 'Your guess is high 👆'
            else:
                message = f'🎉 Correct! You guessed it in {request.session["attempts"]} attempts.'
                request.session['game_over'] = True

            # Check if game over by attempts
            if request.session['attempts'] >= 10 and guess != number:
                message = f'❌ Game Over! The correct number was {number}.'
                request.session['game_over'] = True

        except ValueError:
            message = '⚠️ Please enter a valid number.'

    remaining = max(0, 10 - request.session.get('attempts', 0))

    return render(request, 'game/index.html', {
        'message': message,
        'guess': guess,
        'attempts': request.session.get('attempts', 0),
        'remaining': remaining,
        'game_over': request.session.get('game_over', False)
    })

def reset_game(request):
    request.session.flush()
    return redirect('index')
