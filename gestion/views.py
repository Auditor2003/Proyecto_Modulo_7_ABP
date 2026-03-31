# BENEFICIARIO

class BeneficiarioListView(ListView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_list.html'
    context_object_name = 'beneficiarios'

    # Muestro todos los beneficiarios


class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')

    # Creo un beneficiario


class BeneficiarioUpdateView(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')

    # Edito un beneficiario existente


class BeneficiarioDeleteView(DeleteView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_confirm_delete.html'
    success_url = reverse_lazy('beneficiario_list')

    # Elimino un beneficiario